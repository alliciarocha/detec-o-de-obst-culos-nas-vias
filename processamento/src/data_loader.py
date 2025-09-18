import pandas as pd
import numpy as np
import os
from sklearn.preprocessing import StandardScaler 

def create_windows(data, window_size):
    """
    Cria janelas deslizantes a partir de dados de séries temporais.
    Args:
        data (np.ndarray): Array NumPy 2D com as features (linhas, features).
        window_size (int): Tamanho da janela.
    Returns:
        np.ndarray: Array NumPy 3D com as janelas (num_windows, window_size, num_features).
                    Retorna um array vazio se não houver dados suficientes.
    """
    X = []
    if len(data) < window_size:
        return np.array([]) 

    for i in range(len(data) - window_size + 1):
        X.append(data[i:i + window_size])
    return np.array(X)

# A função load_data agora retornará 4 conjuntos de dados:
# X_train_obstacles, y_train_obstacles: Dados puros dos obstáculos para treino
# X_full_course, y_full_course: Dados completos do percurso para divisão K-Fold
def load_data(train_obstacle_paths, full_course_path, label_map, window_size, features_columns):
    X_train_list = []
    y_train_list = []

    # --- 1. Carregar dados puros para TREINO (30 de cada obstáculo) ---
    print("Iniciando carregamento de dados puros para treino (30 arquivos de cada obstáculo)...")
    for obstacle_name, folder_path in train_obstacle_paths.items():
        label = label_map[obstacle_name]
        all_obstacle_raw_data = [] 

        print(f"  Processando obstáculo: {obstacle_name} (Label: {label})")
        
        for i in range(1, 33): # Ajustado para ir até lobofaixa32.txt
            if obstacle_name == 'lombofaixa':
                file_name = f"lobofaixa{i}.txt" 
            else:
                file_name = f"{obstacle_name}{i}.txt" 

            file_full_path = os.path.join(folder_path, file_name)

            if os.path.exists(file_full_path):
                try:
                    df = pd.read_csv(file_full_path)
                    df.columns = df.columns.str.strip() 
                    
                    missing_cols = [col for col in features_columns if col not in df.columns]
                    if missing_cols:
                        print(f"    AVISO: Arquivo '{file_name}' não possui as colunas esperadas: {missing_cols}. Pulando este arquivo.")
                        continue 
                        
                    features_data = df[features_columns].values
                    all_obstacle_raw_data.append(features_data)
                except Exception as e:
                    print(f"    ERRO ao ler '{file_name}': {e}. Pulando este arquivo.")
            
        if all_obstacle_raw_data:
            concatenated_obstacle_data = np.vstack(all_obstacle_raw_data)
            
            windows_for_obstacle = create_windows(concatenated_obstacle_data, window_size)

            if windows_for_obstacle.size > 0:
                X_train_list.append(windows_for_obstacle)
                y_train_list.append(np.full(len(windows_for_obstacle), label))
                print(f"    Criadas {len(windows_for_obstacle)} janelas para '{obstacle_name}'.")
            else:
                print(f"  AVISO: Nenhuma janela criada para '{obstacle_name}'. Total de linhas de dados brutos: {len(concatenated_obstacle_data)}. Necessário pelo menos {window_size} linhas.")
        else:
            print(f"  AVISO: Nenhum dado válido encontrado para o obstáculo '{obstacle_name}'. Verifique os caminhos e o conteúdo dos arquivos.")


    X_train_obstacles = np.vstack(X_train_list) if X_train_list else np.array([])
    y_train_obstacles = np.hstack(y_train_list) if y_train_list else np.array([])
    
    # --- Escalamento dos dados de treino de obstáculos (Scaler será fitado aqui para ser usado no full_course) ---
    scaler = StandardScaler()
    if X_train_obstacles.size > 0:
        original_train_shape = X_train_obstacles.shape
        X_train_reshaped = X_train_obstacles.reshape(-1, original_train_shape[2])
        X_train_scaled_obstacles = scaler.fit_transform(X_train_reshaped) # FIT e TRANSFORM nos dados de obstaculos
        X_train_scaled_obstacles = X_train_scaled_obstacles.reshape(original_train_shape)
    else:
        X_train_scaled_obstacles = np.array([]) 

    print(f"\nResumo do Treino (Obstáculos Puros): Total de janelas: {X_train_scaled_obstacles.shape if X_train_scaled_obstacles.size > 0 else 'Vazio'}")
    print(f"Resumo do Treino (Obstáculos Puros): Total de rótulos: {y_train_obstacles.shape if y_train_obstacles.size > 0 else 'Vazio'}")


    # --- 2. Carregar dados completos do "percurso completo" (para K-Fold) ---
    windows_full_course_scaled = np.array([]) 
    y_full_course_list = [] # Inicializa como LISTA
    y_full_course = np.array([]) # Inicializa também o array final para caso não entre no IF

    print("\nCarregando dados do 'percurso completo' para K-Fold Cross-Validation...")
    if full_course_path and os.path.exists(full_course_path):
        try:
            full_course_df = pd.read_csv(full_course_path)
            full_course_df.columns = full_course_df.columns.str.strip() 
            
            label_column_name = 'label_id' 
            
            missing_cols_full = [col for col in features_columns + [label_column_name] if col not in full_course_df.columns]
            if missing_cols_full:
                print(f"  ERRO: O arquivo '{full_course_path}' não possui as colunas necessárias: {missing_cols_full}.")
                print("  Não será possível usar o percurso completo.")
                return X_train_scaled_obstacles, y_train_obstacles, np.array([]), np.array([]) 
                
            features_full_course = full_course_df[features_columns].values
            raw_labels_full_course = full_course_df[label_column_name].astype(str).str.strip().values
            
            try:
                labels_full_course = np.array([label_map[label_text] for label_text in raw_labels_full_course])
            except KeyError as e:
                print(f"  ERRO: Rótulo '{e}' encontrado no CSV do percurso completo não está no label_map. Verifique a consistência dos nomes dos rótulos (maiúsculas/minúsculas).")
                print("  Não será possível usar o percurso completo.")
                return X_train_scaled_obstacles, y_train_obstacles, np.array([]), np.array([])

            windows_full_course = create_windows(features_full_course, window_size)
            
            if windows_full_course.size > 0 and X_train_scaled_obstacles.size > 0: 
                original_full_shape = windows_full_course.shape
                windows_full_course_reshaped = windows_full_course.reshape(-1, original_full_shape[2])
                windows_full_course_scaled = scaler.transform(windows_full_course_reshaped) 
                windows_full_course_scaled = windows_full_course_scaled.reshape(original_full_shape)
                print(f"  Janelas do percurso completo carregadas e escaladas: {len(windows_full_course_scaled)}")
            elif windows_full_course.size > 0 and X_train_scaled_obstacles.size == 0:
                print("  AVISO: Dados de obstáculo vazios. Não foi possível escalar o percurso completo com o mesmo scaler.")
                windows_full_course_scaled = np.array([]) 
            else:
                windows_full_course_scaled = np.array([]) 

            # Preencher y_full_course_list como uma lista e converter para NumPy no final
            if len(features_full_course) >= window_size: 
                for i in range(len(features_full_course) - window_size + 1):
                    y_full_course_list.append(labels_full_course[i + window_size - 1]) 
                y_full_course = np.array(y_full_course_list) # CONVERTE para NumPy AQUI
            else:
                y_full_course = np.array([]) 
            
            print(f"  Resumo Percurso Completo (total): X_full_course.shape: {windows_full_course_scaled.shape if windows_full_course_scaled.size > 0 else 'Vazio'}")
            print(f"  Resumo Percurso Completo (total): y_full_course.shape: {y_full_course.shape if y_full_course.size > 0 else 'Vazio'}")
            
        except Exception as e:
            print(f"  ERRO ao carregar ou processar '{full_course_path}': {e}.")
            print("  Não será possível usar o percurso completo.")
    else:
        print(f"AVISO: Caminho do arquivo de percurso completo '{full_course_path}' não fornecido ou arquivo não encontrado.")
        print("Não será possível usar o percurso completo.")

    return X_train_scaled_obstacles, y_train_obstacles, windows_full_course_scaled, y_full_course