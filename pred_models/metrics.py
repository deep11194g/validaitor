import csv
import pickle

import numpy as np
from matplotlib import pyplot as plt
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, classification_report, \
    plot_precision_recall_curve, plot_roc_curve

from validaitor import settings
from pred_models.models import PredModel, get_folder_path

"""
Assumption:
- Prediction is a classification problem
- Predicted Label is always the last row
- Predicted label is 2-class
- All datapoints are numerical in nature
- First two columns are row identifiers (ignored as feature)
"""


def csv_to_dataset(csv_file_path):
    X = []
    Y = []
    feature_labels = []
    with open(file=csv_file_path, mode='r') as csv_file:
        for idx, row in enumerate(csv.reader(csv_file)):
            if idx == 0:
                feature_labels = row[2:-1]
                continue
            try:
                Y.append(int(row[-1]))
                feature_vals = []
                for cell in row[2:-1]:
                    feature_vals.append(float(cell))
                X.append(feature_vals)
            except TypeError:
                continue
    return np.array(X), np.array(Y), feature_labels


def generate(pred_model):
    """

    :param(PredModel) pred_model:
    """
    if not pred_model:
        return
    loaded_clf = pickle.load(open(pred_model.trained_model.path, mode="rb"))
    X_test, Y_test, feature_labels = csv_to_dataset(pred_model.test_set.path)
    X_train, Y_train, _ = csv_to_dataset(pred_model.train_set.path)
    loaded_clf.fit(X_train, Y_train)
    return performance(X_test, Y_test, loaded_clf, pred_model, feature_labels)


def performance(X_test, y_test, clf, pred_model, feature_labels):
    """

    :param(np.array) X_test:
    :param(np.array) y_test:
    :param clf:
    :param(PredModel) pred_model:
    :param(list of str) feature_labels:
    """
    pred_model.features = feature_labels

    y_pred = clf.predict(X_test)

    # Confusion Matrix
    cf = confusion_matrix(y_true=y_test, y_pred=y_pred, normalize='true')
    disp = ConfusionMatrixDisplay(confusion_matrix=cf)
    disp.plot(cmap='Blues')
    plt.title('Confusion Matrix - {}'.format(pred_model.name))
    plt_path = "{}.png".format(get_folder_path(pred_model, 'confusion_matrix'))
    plt.savefig(settings.MEDIA_ROOT + '/' + plt_path)
    pred_model.confusion_matrix = plt_path

    # Classification Report
    pred_model.classification_report = classification_report(y_test, y_pred, digits=3)

    # PRC Plot
    plot_precision_recall_curve(clf, X_test, y_test, name=pred_model.name)
    plt.ylim(0, 1)
    plt_path = "{}.png".format(get_folder_path(pred_model, 'prc_plot'))
    plt.savefig(settings.MEDIA_ROOT + '/' + plt_path)
    pred_model.prc_plot = plt_path

    plot_roc_curve(clf, X_test, y_test, name=pred_model.name)
    plt.ylim(0, 1)
    plt_path = "{}.png".format(get_folder_path(pred_model, 'roc_plot'))
    plt.savefig(settings.MEDIA_ROOT + '/' + plt_path)
    pred_model.roc_plot = plt_path

    pred_model.save()

    return pred_model
