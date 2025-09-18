from keras._tf_keras.keras.callbacks import EarlyStopping, ModelCheckpoint
import numpy as np


def train_lstm_model(model, X_train, y_train, X_val=None, y_val=None, epochs=50, batch_size=32, model_save_path='best_model.h5', class_weight=None, callbacks=None): # <--- CORRIGIDO AQUI! Adicionado 'callbacks=None'
    """
    Treina o modelo LSTM.

    Args:
        model (tensorflow.keras.Model): O modelo LSTM compilado a ser treinado.
        X_train (np.ndarray): Dados de treino.
        y_train (np.ndarray): Rótulos de treino.
        X_val (np.ndarray, optional): Dados de validação. Padrão para None.
        y_val (np.ndarray, optional): Rótulos de validação. Padrão para None.
        epochs (int): Número de épocas para treinar. Padrão para 50.
        batch_size (int): Tamanho do batch para treinamento. Padrão para 32.
        model_save_path (str): Caminho para salvar o melhor modelo (com base na acurácia de validação).
        class_weight (dict, optional): Dicionário de pesos de classe. Padrão para None.
        callbacks (list, optional): Lista de callbacks a serem usados durante o treinamento. Padrão para None. # <--- Descrição do novo argumento
    """

    # Garante que callbacks_list é uma lista se for None
    if callbacks is None:
        callbacks_list = []
    else:
        callbacks_list = list(callbacks) # Converte para lista mutável

    validation_data = None
    if X_val is not None and y_val is not None and X_val.size > 0 and y_val.size > 0:
        validation_data = (X_val, y_val)
        print(f"\nTreinando modelo com validação em {len(X_val)} amostras de validação.")

        early_stopping = EarlyStopping(monitor='val_accuracy', patience=30, mode='max', verbose=1) 
        callbacks_list.append(early_stopping) # Adiciona ao callbacks_list

        model_checkpoint = ModelCheckpoint(
            filepath=model_save_path,
            monitor='val_accuracy',
            mode='max',
            save_best_only=True,
            verbose=1
        )
        callbacks_list.append(model_checkpoint) # Adiciona ao callbacks_list
    else:
        print("\nTreinando modelo SEM conjunto de validação. EarlyStopping e ModelCheckpoint baseados em validação não serão usados.")

    print(f"Iniciando treinamento por até {epochs} épocas com batch_size={batch_size}...")

    history = model.fit(
        X_train, y_train,
        epochs=epochs,
        batch_size=batch_size,
        validation_data=validation_data,
        callbacks=callbacks_list, # <--- Passando a lista de callbacks (que agora inclui EarlyStopping/ModelCheckpoint)
        class_weight=class_weight, 
        verbose=1 
    )

    print("\nTreinamento concluído.")
    return history