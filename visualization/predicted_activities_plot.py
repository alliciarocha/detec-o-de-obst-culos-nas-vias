import matplotlib.pyplot as plt
import numpy as np
import os

def plot_predicted_activities(y_true, y_pred, class_names, title='Predicted Activities', save_path=None):
    plt.figure(figsize=(10, 6))

    # Mapeia os rótulos numéricos para os nomes das classes para o eixo Y
    y_ticks = np.arange(len(class_names))

    # Plota os dados verdadeiros
    plt.step(range(len(y_true)), y_true, where='post', label='Test Data', color='red', alpha=0.7)

    # Plota as previsões do modelo
    plt.step(range(len(y_pred)), y_pred, where='post', label='Predicted', color='blue', alpha=0.7)

    plt.yticks(y_ticks, class_names)
    plt.ylim(-0.5, len(class_names) - 0.5) # Ajusta os limites do eixo Y
    plt.title(title)
    plt.xlabel('Timestep') # Ou 'Timestamp' se você tivesse os dados brutos de tempo
    plt.ylabel('Activity')
    plt.legend()
    plt.grid(True)

    if save_path:
        plt.savefig(save_path)
        print(f"Gráfico '{title}' salvo em: {save_path}")

    plt.show()
    plt.close(plt.gcf())