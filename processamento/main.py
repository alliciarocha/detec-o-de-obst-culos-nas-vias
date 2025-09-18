import os
import sys
import numpy as np
import matplotlib.pyplot as plt 
from sklearn.metrics import classification_report 
from sklearn.utils import class_weight 
from keras._tf_keras.keras.models import load_model 
from sklearn.model_selection import StratifiedKFold, train_test_split

# --- Configurações de Pastas ---
os.makedirs('reports', exist_ok=True)
os.makedirs('saved_models', exist_ok=True) 
os.makedirs('visualization', exist_ok=True) 

script_dir = os.path.dirname(__file__)
project_root = script_dir 
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Importa as funções dos módulos que criamos
from src.data_loader import load_data
# Escolha o modelo a ser criado (descomente apenas um)
# from models.lstm_model import create_lstm_model 
from models.bi_lstm_model import create_bi_lstm_model as create_lstm_model
# from models.gru_model import create_gru_model as  create_lstm_model 

from training.model_trainer import train_lstm_model
from training.metrics_callback import MetricsPerClassCallback 
from utils.plot_history import plot_training_history
    
# --- CONFIGURAÇÕES DE DADOS E CAMINHOS ---
train_obstacle_paths = {
    'quebramola': os.path.join('OBSTÁCULOS', 'Data', 'quebraMola'),
    'buraco': os.path.join('OBSTÁCULOS', 'Data', 'buraco'),
    'buracoMaior': os.path.join('OBSTÁCULOS', 'Data', 'buracoMaior'),
    'lombofaixa': os.path.join('OBSTÁCULOS', 'Data', 'lobofaixa'), 
    'tartaruga': os.path.join('OBSTÁCULOS', 'Data', 'tartaruga')
}

full_course_data_path = os.path.join('dataset', 'percurso_completo.csv') 

label_map = {
    'quebramola': 0,
    'buraco': 1,
    'buracoMaior': 2,
    'lombofaixa': 3,
    'tartaruga': 4,
    'normal': 5 
}

features_cols = ['accX', 'accY', 'accZ', 'gyroX', 'gyroY', 'gyroZ'] 

window_size = 20 

# --- CARREGAMENTO DE DADOS INICIAIS (para K-Fold) ---
# load_data agora retorna os dados de obstáculos puros e os dados completos do percurso completo
X_train_obstacles_pure, y_train_obstacles_pure, X_full_course_context, y_full_course_context = load_data(
    train_obstacle_paths=train_obstacle_paths,
    full_course_path=full_course_data_path, 
    label_map=label_map,
    window_size=window_size,
    features_columns=features_cols
)

# Combine todos os dados disponíveis em um único conjunto para o K-Fold
# É crucial que as classes para estratificação estejam presentes
if X_train_obstacles_pure.size > 0 and X_full_course_context.size > 0:
    X_combined = np.vstack([X_train_obstacles_pure, X_full_course_context])
    y_combined = np.hstack([y_train_obstacles_pure, y_full_course_context])
elif X_train_obstacles_pure.size > 0: # Se só houver dados puros de obstáculo
    X_combined = X_train_obstacles_pure
    y_combined = y_train_obstacles_pure
    print("AVISO: Percurso completo não carregado. K-Fold será baseado apenas em dados puros de obstáculos.")
elif X_full_course_context.size > 0: # Se só houver dados do percurso completo
    X_combined = X_full_course_context
    y_combined = y_full_course_context
    print("AVISO: Dados puros de obstáculos não carregados. K-Fold será baseado apenas no percurso completo.")
else:
    print("\nERRO: Nenhum dado foi carregado para o K-Fold.")
    sys.exit("Encerrando o script.")

n_timesteps = window_size
n_features = features_cols[0].shape[0] if isinstance(features_cols[0], list) else len(features_cols) 
if X_combined.size > 0: # Pega da dimensão do conjunto combinado
    n_features = X_combined.shape[2] 
n_outputs = len(label_map) 

print(f"\nConfiguração Geral: timesteps={n_timesteps}, features={n_features}, outputs={n_outputs}")
print(f"Total de amostras para K-Fold: {X_combined.shape[0]}")
print(f"Distribuição de classes para K-Fold: {dict(zip(label_map.keys(), np.bincount(y_combined.astype(int))))}")


# --- CONFIGURAÇÕES K-FOLD ---
n_splits = 5 # Número de folds. 5 é um valor comum.
# Garante que a estratificação use a distribuição de todas as classes no conjunto combinado
skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)

# Listas para armazenar resultados de cada fold
fold_accuracies = []
fold_losses = []
fold_reports = [] 

# --- PARÂMETROS DO MODELO (CONFIRME SE SÃO OS SEUS VALORES REAIS!) ---
# Estes são os valores que funcionaram bem para a acurácia de 79.41% e loss baixa.
# Assumindo estes valores, por favor, verifique-os nos seus arquivos.
current_learning_rate = 0.001 # <--- SEU LEARNING RATE DO BI-LSTM (79% accuracy)
current_patience = 30 # <--- SUA PATIENCE DO BI-LSTM (79% accuracy)
current_epochs = 200 # <--- Aumentado para dar mais chance ao EarlyStopping
    
# --- LOOP K-FOLD ---
print(f"\nIniciando K-Fold Cross-Validation com {n_splits} folds...")
    
# Gerar os splits (índices) para o K-Fold
if len(np.unique(y_combined)) <= 1:
    print("ERRO: Apenas uma classe encontrada no conjunto combinado para K-Fold. Não é possível estratificar.")
    sys.exit("Encerrando: K-Fold estratificado requer múltiplas classes.")

for fold, (train_val_index, test_index) in enumerate(skf.split(X_combined, y_combined)):
    print(f"\n--- Iniciando Fold {fold + 1}/{n_splits} ---")

    # Dados de Treino/Validação e Teste para o Fold Atual
    X_train_val_fold, X_test_fold = X_combined[train_val_index], X_combined[test_index]
    y_train_val_fold, y_test_fold = y_combined[train_val_index], y_combined[test_index]

    # Dividir o conjunto de Treino/Validação do Fold em Treino e Validação Finais (80/20 do treino do fold)
    stratify_inner_split = y_train_val_fold if len(np.unique(y_train_val_fold)) > 1 else None
    
    if X_train_val_fold.size > 0:
        X_train_fold, X_val_fold, y_train_fold, y_val_fold = train_test_split(
            X_train_val_fold, y_train_val_fold, test_size=0.2, random_state=42, stratify=stratify_inner_split
        )
    else:
        print(f"AVISO: X_train_val_fold vazio no Fold {fold + 1}. Pulando este fold.")
        continue 

    print(f"  Shape Treino (Fold {fold + 1}): {X_train_fold.shape}, Rótulos: {y_train_fold.shape}")
    print(f"  Shape Validação (Fold {fold + 1}): {X_val_fold.shape}, Rótulos: {y_val_fold.shape}")
    print(f"  Shape Teste (Fold {fold + 1}): {X_test_fold.shape}, Rótulos: {y_test_fold.shape}")
    
    # Calcule os pesos de classe para o y_train_fold deste fold
    classes_in_fold_train = np.unique(y_train_fold)
    if len(classes_in_fold_train) > 1: 
        pesos_calculados_fold = class_weight.compute_class_weight(
            class_weight='balanced',
            classes=classes_in_fold_train,
            y=y_train_fold
        )
        class_weights_fold = dict(zip(classes_in_fold_train, pesos_calculados_fold))
    else: 
        class_weights_fold = None
        print(f"  AVISO: Apenas uma classe no treino do Fold {fold+1}. Não usando class_weight.")

    # Crie um novo modelo para cada fold para garantir que não haja aprendizado cruzado
    model = create_lstm_model(n_timesteps, n_features, n_outputs) 

    model_save_path_fold = os.path.join('saved_models', f'best_model_fold_{fold+1}.h5')
    
    # --- Configuração dos Callbacks para o Fold ---
    callbacks_list_fold = [] 

    metrics_callback_instance_fold = None
    if X_val_fold.size > 0 and y_val_fold.size > 0:
        metrics_callback_instance_fold = MetricsPerClassCallback(
            X_val=X_val_fold, 
            y_val=y_val_fold, 
            class_names=list(label_map.keys()), 
            save_report_path=os.path.join('reports', f'epoch_classification_report_fold_{fold+1}.txt')
        )
        callbacks_list_fold.append(metrics_callback_instance_fold)
    
    # Treine o modelo para o fold atual
    history_fold = train_lstm_model( 
        model, 
        X_train_fold, 
        y_train_fold, 
        X_val=X_val_fold, 
        y_val=y_val_fold, 
        epochs=current_epochs, 
        batch_size=32, 
        model_save_path=model_save_path_fold,
        class_weight=class_weights_fold, 
        callbacks=callbacks_list_fold 
    )
    
    # Avalie o modelo no conjunto de teste deste fold
    print(f"\n--- Avaliação do Modelo no Teste do Fold {fold + 1} ---")
    best_model_fold = load_model(model_save_path_fold)
    
    loss_fold, accuracy_fold = best_model_fold.evaluate(X_test_fold, y_test_fold, verbose=0)
    print(f"  Acurácia: {accuracy_fold:.4f}")
    print(f"  Loss: {loss_fold:.4f}")

    # Armazene os resultados
    fold_accuracies.append(accuracy_fold)
    fold_losses.append(loss_fold)

    # Gera e armazena o Classification Report para este fold
    y_pred_probs_fold = best_model_fold.predict(X_test_fold, verbose=0)
    y_pred_fold = np.argmax(y_pred_probs_fold, axis=1)
    report_fold = classification_report(y_test_fold, y_pred_fold, target_names=list(label_map.keys()), zero_division=0)
    fold_reports.append(report_fold)
    print(f"  Relatório de Classificação para o Fold {fold + 1}:\n{report_fold}")

    # Opcional: Plotar histórico e matriz de confusão para cada fold (comentado para evitar muitas janelas)
    if history_fold is not None:
        plot_training_history(history_fold, title=f'Histórico de Treino Fold {fold+1}', 
                              save_path=os.path.join('reports', f'training_history_fold_{fold+1}.png'))
    try:
        from visualization.confusion_matrix_plot import plot_confusion_matrix
        plot_confusion_matrix(y_test_fold, y_pred_fold, class_names=list(label_map.keys()), 
                              title=f'Matriz de Confusão Fold {fold+1}',
                              save_path=os.path.join('reports', f'confusion_matrix_fold_{fold+1}.png'))
    except ImportError:
        print(f"AVISO: Não foi possível plotar CM para o Fold {fold+1}.") 
    except Exception as e:
        print(f"ERRO ao plotar ou salvar CM para o Fold {fold+1}: {e}") # Mais detalhado para erro CM plot/save

# --- Resultados Finais MÉDIOS do K-Fold ---
print("\n\n--- Resultados Finais do K-Fold Cross-Validation ---")
print(f"Acurácia Média ({n_splits} folds): {np.mean(fold_accuracies):.4f} +/- {np.std(fold_accuracies):.4f}")
print(f"Loss Média ({n_splits} folds): {np.mean(fold_losses):.4f} +/- {np.std(fold_losses):.4f}")

# Salva os resultados médios em um arquivo de relatório final
with open(os.path.join('reports', 'kfold_summary.txt'), 'w') as f:
    f.write(f"Resultados Finais do K-Fold Cross-Validation ({n_splits} folds):\n")
    f.write(f"Acurácia Média: {np.mean(fold_accuracies):.4f} +/- {np.std(fold_accuracies):.4f}\n")
    f.write(f"Loss Média: {np.mean(fold_losses):.4f} +/- {np.std(fold_losses):.4f}\n\n")
    f.write("Relatórios Detalhados por Fold:\n")
    for i, report_str in enumerate(fold_reports):
        f.write(f"\n--- Fold {i+1} ---\n{report_str}\n")
print(f"Sumário K-Fold salvo em: {os.path.join('reports', 'kfold_summary.txt')}")


print("\nScript main.py concluído.")