import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix
import numpy as np

def plot_confusion_matrix(y_true, y_pred, class_names, title='Matriz de Confusão', save_path=None): 
    cm = confusion_matrix(y_true, y_pred)

    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", 
                xticklabels=class_names, yticklabels=class_names)

    plt.title(title)
    plt.ylabel('Real')
    plt.xlabel('Valor Predito')

    if save_path: 
        plt.savefig(save_path)
        print(f"Matriz de Confusão '{title}' salva em: {save_path}")

    #plt.show() # Mostra o gráfico
    plt.close(plt.gcf()) 