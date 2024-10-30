import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc, precision_recall_curve, average_precision_score, accuracy_score, \
confusion_matrix, classification_report
from sklearn.calibration import calibration_curve
import itertools
from sklearn.metrics import roc_auc_score, accuracy_score, confusion_matrix, classification_report


def plot_roc_curve(final_model, X_test_final_scaled, y_test, title,labels=['No dementia','dementia']):
    colors = ['green', 'blue']
    plt.figure(figsize=(8, 6))

    for i in range(2):
        y_pred_proba = final_model.predict_proba(X_test_final_scaled)[:, i]
        fpr, tpr, _ = roc_curve(y_test[:, i], y_pred_proba)
        roc_auc = auc(fpr, tpr)
        if i!=0:
            plt.plot(fpr, tpr, color=colors[i], lw=2, label=f'ROC curve (AUC {labels[i]}={roc_auc:.2f})')

    plt.plot([0, 1], [0, 1], color='red', lw=2, linestyle='--', label='Random')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title(title)
    plt.legend(loc="lower right")
    plt.show()

def plot_precision_recall_curve(final_model, X_test_final_scaled, y_test, title,labels=['No dementia','dementia']):
    colors = ['green', 'blue']
    plt.figure(figsize=(8, 6))

    for i in range(2):
        y_pred_proba = final_model.predict_proba(X_test_final_scaled)[:, i]
        precision, recall, _ = precision_recall_curve(y_test[:, i], y_pred_proba)
        auprc = average_precision_score(y_test[:, i], y_pred_proba)
        plt.plot(recall, precision, color=colors[i], lw=2, label=f'Precision-Recall curve (AUPRC {labels[i]}={auprc:.2f})')

    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.title(title)
    plt.legend(loc='lower left')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.grid(True)
    plt.show()


def plot_confusion_matrix(cm, classes, title, cmap=plt.cm.Blues):
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    thresh = cm.max() / 2.0
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], 'd'),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.show()
    

