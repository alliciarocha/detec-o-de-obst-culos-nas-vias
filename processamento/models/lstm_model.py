from keras._tf_keras.keras.models import Sequential
from keras._tf_keras.keras.layers import LSTM, Dense, Dropout
from keras._tf_keras.keras.optimizers import Adam

def create_lstm_model(n_timesteps, n_features, n_outputs):
    model = Sequential()
    optimizer = Adam(learning_rate=0.00001)
    # Primeira camada LSTM: Aumente units, mantenha return_sequences=True
    model.add(LSTM(units=150, activation='relu', input_shape=(n_timesteps, n_features), return_sequences=True))
    model.add(Dropout(0.3)) 

    # Segunda camada LSTM: Mantenha return_sequences=True para adicionar uma terceira
    model.add(LSTM(units=150, activation='relu', return_sequences=True)) 
    model.add(Dropout(0.3))

    # Terceira camada LSTM (nova): return_sequences=False na última antes de Dense
    model.add(LSTM(units=100, activation='relu')) 
    model.add(Dropout(0.3))


    model.add(Dense(units=n_outputs, activation='softmax'))

    model.compile(optimizer, loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    print("\nModelo LSTM criado com sucesso:")
    model.summary() 

    return model