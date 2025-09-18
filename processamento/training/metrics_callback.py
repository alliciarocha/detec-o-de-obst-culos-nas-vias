from sklearn.metrics import classification_report
from keras._tf_keras.keras.callbacks import Callback
import numpy as np
import os 
from visualization.confusion_matrix_plot import plot_confusion_matrix 

class MetricsPerClassCallback(Callback):
    def __init__(self, X_val, y_val, class_names=None, save_report_path=None, save_confusion_matrix_path=None):
        super().__init__()
        self.X_val = X_val
        self.y_val = y_val
        self.class_names = class_names
        self.save_report_path = save_report_path
        self.save_confusion_matrix_path = save_confusion_matrix_path

        # Garante que o diretório de salvamento do relatório existe
        if self.save_report_path:
            os.makedirs(os.path.dirname(self.save_report_path), exist_ok=True)
            # Limpa o arquivo de relatório a cada nova execução de treinamento
            with open(self.save_report_path, "w") as f:
                f.write("Relatórios de Classificação por Época:\n")

    def on_epoch_end(self, epoch, logs=None):
        # Previsões no conjunto de validação
        y_pred_probs = self.model.predict(self.X_val, verbose=0) # verbose=0 para não poluir o terminal
        y_pred = np.argmax(y_pred_probs, axis=1)

        # Rótulos verdadeiros (garante que y_val está no formato correto)
        y_true = self.y_val if len(self.y_val.shape) == 1 else np.argmax(self.y_val, axis=1)

        # Gera o relatório de classificação
        report = classification_report(y_true, y_pred, target_names=self.class_names, digits=4, zero_division=0)

        print(f"\n[Epoca {epoch + 1}] Relatório de Classificação na Validação:\n{report}")

        # Salva o relatório em arquivo, se o caminho for fornecido
        if self.save_report_path:
            with open(self.save_report_path, "a") as f:
                f.write(f"\n[Epoca {epoch + 1}]\n{report}\n")

        pass 