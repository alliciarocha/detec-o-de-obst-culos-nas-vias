from keras._tf_keras.keras.models import Sequential
from keras._tf_keras.keras.layers import LSTM, Dense, Dropout, Bidirectional
from keras._tf_keras.keras.optimizers import Adam
from keras._tf_keras.keras.callbacks import EarlyStopping, ModelCheckpoint
import numpy as np

def create_bi_lstm_model(n_timesteps, n_features, n_outputs, learning_rate=0.001):
    """
    Cria e compila um modelo Bi-LSTM aprimorado para classificação de séries temporais.

    Args:
        n_timesteps (int): Número de passos de tempo na entrada (janela de tempo).
        n_features (int): Número de características em cada passo de tempo.
        n_outputs (int): Número de classes de saída.
        learning_rate (float): Taxa de aprendizado para o otimizador Adam.
    
    Returns:
        keras.Model: O modelo Bi-LSTM compilado.
    """
    model = Sequential()

    # Primeira camada Bi-LSTM. 'return_sequences=True' é essencial para empilhar camadas LSTM.
    # Aumentamos o número de unidades para uma maior capacidade de aprendizado.
    model.add(Bidirectional(LSTM(units=150, activation='relu', input_shape=(n_timesteps, n_features), return_sequences=True)))
    model.add(Dropout(0.3)) 

    # Segunda camada Bi-LSTM, mantendo 'return_sequences=True'.
    model.add(Bidirectional(LSTM(units=100, activation='relu', return_sequences=True))) 
    model.add(Dropout(0.3))

    # Terceira camada Bi-LSTM. 'return_sequences=False' por padrão na última camada
    # para que a saída seja um vetor 1D para a camada densa.
    model.add(Bidirectional(LSTM(units=50, activation='relu'))) 
    model.add(Dropout(0.3))

    # Camada densa de saída com ativação softmax para classificação multi-classe.
    # O número de unidades deve ser igual ao número de classes.
    model.add(Dense(units=n_outputs, activation='softmax'))

    # Otimizador Adam com taxa de aprendizado ajustável
    optimizer = Adam(learning_rate=learning_rate) 
    
    # Compila o modelo. 'sparse_categorical_crossentropy' é ideal para labels inteiros (0, 1, 2...).
    model.compile(optimizer=optimizer, loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    print("\nModelo Bi-LSTM criado com sucesso:") 
    model.summary() 

    return model

# Exemplo de como usar o modelo e callbacks
if __name__ == '__main__':
    # =========================================================================
    # Configuração de Hiperparâmetros
    # =========================================================================
    timesteps = 20  # Número de amostras por janela de tempo
    features = 7    # Número de características (ex: accX, accY, accZ, gyroX, gyroY, gyroZ, etc.)
    num_classes = 6 # Número total de classes de saída (ex: normal, curva, 4 obstáculos)
    learning_rate = 0.0001
    
    # =========================================================================
    # Criação e Compilação do Modelo
    # =========================================================================
    # A função foi ajustada para aceitar o número correto de classes.
    model = create_bi_lstm_model(n_timesteps=timesteps, n_features=features, n_outputs=num_classes, learning_rate=learning_rate)

    # =========================================================================
    # Simulação de Dados de Treinamento
    # =========================================================================
    # Para rodar o exemplo, simulamos dados de treino e validação.
    # Na sua aplicação real, você substituiria esta parte pelos seus dados X e y.
    
    # Crie dados de treino e validação simulados (substitua por seus dados reais)
    num_samples = 1000
    X_train = np.random.rand(num_samples, timesteps, features)
    y_train = np.random.randint(0, num_classes, size=(num_samples,)) # Labels de 0 a (num_classes-1)

    X_val = np.random.rand(num_samples // 4, timesteps, features)
    y_val = np.random.randint(0, num_classes, size=(num_samples // 4,))

    # =========================================================================
    # Configuração de Callbacks
    # =========================================================================
    # EarlyStopping para parar o treinamento quando o val_loss parar de melhorar.
    early_stopping = EarlyStopping(
        monitor='val_loss', 
        patience=10,        # Número de épocas sem melhoria para parar
        restore_best_weights=True  # Restaura os pesos do melhor modelo
    )

    # ModelCheckpoint para salvar o modelo com o melhor val_loss
    model_checkpoint = ModelCheckpoint(
        'best_model.keras', 
        save_best_only=True, # Salva apenas o melhor modelo
        monitor='val_loss', 
        mode='min'          # Monitora a perda de validação (menor é melhor)
    )

    # =========================================================================
    # Treinamento do Modelo com Callbacks
    # =========================================================================
    print("\nIniciando o treinamento do modelo...")
    history = model.fit(
        X_train, 
        y_train, 
        epochs=100, 
        batch_size=32,
        validation_data=(X_val, y_val),
        callbacks=[early_stopping, model_checkpoint]
    )

    print("\nTreinamento concluído. O melhor modelo foi salvo em 'best_model.keras'")