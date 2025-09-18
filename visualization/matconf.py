import numpy as np
import matplotlib.pyplot as plt

def plot_confusion_matrix(cm, class_names, title="Matriz de Confusão", normalize=False,
                          save_path=None, fmt=None, figsize=(4, 3), dpi=300, vmin=None, vmax=None):
    if normalize:
        with np.errstate(all='ignore'):
            row_sums = cm.sum(axis=1, keepdims=True)
            cm_display = np.divide(cm, row_sums, where=row_sums != 0)
        # for normalized, force scale 0..1 for comparabilidade
        vmin = 0.0
        vmax = 1.0
    else:
        cm_display = cm

    fig, ax = plt.subplots(figsize=figsize)
    im = ax.imshow(cm_display, interpolation="nearest", cmap=plt.cm.Blues,
                   vmin=vmin, vmax=vmax)
    cbar = fig.colorbar(im, ax=ax)
    cbar.ax.tick_params(labelsize=8)

    ax.set(
        xticks=np.arange(len(class_names)),
        yticks=np.arange(len(class_names)),
        xticklabels=class_names,
        yticklabels=class_names,
        xlabel="Classe Prevista",
        ylabel="Classe Real",
        title=title
    )
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", fontsize=8)
    plt.setp(ax.get_yticklabels(), fontsize=8)
    ax.xaxis.label.set_size(9)
    ax.yaxis.label.set_size(9)
    ax.title.set_size(10)

    thresh = (cm_display.max() / 2.0) if cm_display.max() != 0 else 0

    for i in range(cm_display.shape[0]):
        for j in range(cm_display.shape[1]):
            if normalize:
                text = f"{cm_display[i, j]:.2f}"
            else:
                text = f"{cm[i, j]}"
            ax.text(j, i, text,
                    ha="center", va="center",
                    fontsize=7,
                    color="white" if cm_display[i, j] > thresh else "black")

    fig.tight_layout()

    if save_path:
        if fmt is None:
            fmt = save_path.split('.')[-1]
        if fmt.lower() in ['pdf', 'svg']:
            fig.savefig(save_path, format=fmt, bbox_inches='tight')
        else:
            fig.savefig(save_path, format=fmt, dpi=dpi, bbox_inches='tight')
        print(f"Salvo em: {save_path}")

    plt.close(fig)


# === Dados e nomes ===
class_names = ['quebra-molas', 'buraco A', 'buraco B', 'lombofaixa', 'tartaruga', 'normal']

# LSTM
cm_lstm = np.array([
    [208, 0,   0,   0,   0, 0],
    [0,   100, 0,   0,   0, 0],
    [0,   1,   129, 0,   0, 4],
    [0,   1,   0,   158, 0, 0],
    [0,   0,   0,   0,   86, 0],
    [0,   0,   0,   0,   2, 33],
])

# Bi-LSTM
cm_bilstm = np.array([
    [205, 0,   0,   0,   0, 3],
    [0,   100, 0,   0,   0, 0],
    [0,   0,   129, 0,   0, 5],
    [2,   0,   0,   154, 3, 0],
    [0,   0,   0,   1,   85, 0],
    [0,   0,   0,   2,   1, 32],
])

# GRU
cm_gru = np.array([
    [207, 0,   0,   0,   1, 0],
    [0,   100, 0,   0,   0, 0],
    [0,   1,   133, 0,   0, 0],
    [0,   0,   1,   158, 0, 0],
    [0,   0,   0,   0,   86, 0],
    [0,   0,   0,   1,   0, 34],
])

# Salva cada matriz (absoluta e normalizada) com nomes distintos
plot_confusion_matrix(cm_lstm, class_names,
                      title="Matriz de Confusão do Modelo LSTM (Absoluta)",
                      normalize=False,
                      save_path="confusion_lstm_absoluto.png")
plot_confusion_matrix(cm_lstm, class_names,
                      title="Matriz de Confusão Normalizada do Modelo LSTM",
                      normalize=True,
                      save_path="confusion_lstm_normalizada.png")
plot_confusion_matrix(cm_lstm, class_names,
                      title="Matriz de Confusão Normalizada do Modelo LSTM",
                      normalize=True,
                      save_path="confusion_lstm_normalizada.pdf")  # vetor

plot_confusion_matrix(cm_bilstm, class_names,
                      title="Matriz de Confusão do Modelo Bi-LSTM (Absoluta)",
                      normalize=False,
                      save_path="confusion_bilstm_absoluto.png")
plot_confusion_matrix(cm_bilstm, class_names,
                      title="Matriz de Confusão Normalizada do Modelo Bi-LSTM",
                      normalize=True,
                      save_path="confusion_bilstm_normalizada.png")
plot_confusion_matrix(cm_bilstm, class_names,
                      title="Matriz de Confusão Normalizada do Modelo Bi-LSTM",
                      normalize=True,
                      save_path="confusion_bilstm_normalizada.pdf")

plot_confusion_matrix(cm_gru, class_names,
                      title="Matriz de Confusão do Modelo GRU (Absoluta)",
                      normalize=False,
                      save_path="confusion_gru_absoluto.png")
plot_confusion_matrix(cm_gru, class_names,
                      title="Matriz de Confusão Normalizada do Modelo GRU",
                      normalize=True,
                      save_path="confusion_gru_normalizada.png")
plot_confusion_matrix(cm_gru, class_names,
                      title="Matriz de Confusão Normalizada do Modelo GRU",
                      normalize=True,
                      save_path="confusion_gru_normalizada.pdf")
