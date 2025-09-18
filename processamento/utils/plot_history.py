import matplotlib.pyplot as plt

def plot_training_history(history, title='Training History', save_path=None):
    has_val_data = 'val_accuracy' in history.history and 'val_loss' in history.history

    plt.figure(figsize=(12, 5))

    plt.subplot(1, 2, 1)
    plt.plot(history.history['loss'], label='Train Loss')
    if has_val_data:
        plt.plot(history.history['val_loss'], label='Validation Loss')
    plt.title(f'{title} - Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()
    plt.grid(True)

    plt.subplot(1, 2, 2)
    plt.plot(history.history['accuracy'], label='Train Accuracy')
    if has_val_data:
        plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
    plt.title(f'{title} - Accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.legend()
    plt.grid(True)

    plt.tight_layout()

    if save_path: 
        plt.savefig(save_path)
        print(f"Gráfico '{title}' salvo em: {save_path}")

    #plt.show() 
    plt.close(plt.gcf())