from keras._tf_keras.keras.models import Sequential
from keras._tf_keras.keras.layers import GRU, Dense, Dropout
from keras._tf_keras.keras.optimizers import Adam

def create_gru_model(n_timesteps, n_features, n_outputs): 
    model = Sequential()

    model.add(GRU(units=150, activation='relu', input_shape=(n_timesteps, n_features), return_sequences=True))
    model.add(Dropout(0.3)) # <--- Aumentar dropout se overfitting for um problema

    model.add(GRU(units=150, activation='relu', return_sequences=True)) 
    model.add(Dropout(0.3))

    model.add(GRU(units=100, activation='relu')) 
    model.add(Dropout(0.3))

    model.add(Dense(units=n_outputs, activation='softmax'))

    optimizer = Adam(learning_rate=0.001) 
    model.compile(optimizer=optimizer, loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    print("\nModelo GRU criado com sucesso:")
    model.summary() 

    return model