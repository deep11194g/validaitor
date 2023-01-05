import csv
import pickle

import numpy as np
from matplotlib import pyplot as plt
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, classification_report, \
    plot_precision_recall_curve, plot_roc_curve

from django.conf import settings
from pred_models.models import get_folder_path

plt.switch_backend('Agg')

"""
Assumption:
- Prediction is a classification problem
- Predicted Label is always the last row
- Predicted label is 2-class
- All datapoints are numerical in nature
- First two columns are row identifiers (ignored as feature)
"""


def csv_to_dataset(csv_file_path):
    """
    Read a CSV dataset file for test or train and output data in form of usage by models

    :param (str) csv_file_path: Path tp CSV file for test/train datasets
    :return (list of list, list, list of str): Feature dataset, prediction label, feature labels
    """
    X = []
    y = []
    feature_labels = []
    with open(file=csv_file_path, mode='r') as csv_file:
        for idx, row in enumerate(csv.reader(csv_file)):
            if idx == 0:
                feature_labels = row[1:-1]
                continue
            try:
                y.append(int(row[-1]))
                feature_vals = []
                for cell in row[1:-1]:
                    feature_vals.append(float(cell))
                X.append(feature_vals)
            except TypeError:
                continue
    return np.array(X), np.array(y), feature_labels


class PerformanceStatsAnalyser:
    def __init__(self, pred_model_obj):
        self.pred_model_obj = pred_model_obj
        self.loaded_clf = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.feature_labels = None

    def load(self):
        """
        Load data into class variables
        """
        self.loaded_clf = pickle.load(open(self.pred_model_obj.trained_model.path, mode="rb"))
        self.X_test, self.y_test, self.feature_labels = csv_to_dataset(self.pred_model_obj.test_set.path)
        self.X_train, self.y_train, _ = csv_to_dataset(self.pred_model_obj.train_set.path)

    def performance(self):
        """
        Compute and store model's performance stats
        """
        y_pred = self.loaded_clf.predict(self.X_test)

        # Confusion Matrix
        cf = confusion_matrix(y_true=self.y_test, y_pred=y_pred, normalize='true')
        disp = ConfusionMatrixDisplay(confusion_matrix=cf)
        disp.plot(cmap='Blues')
        plt.title('Confusion Matrix - {}'.format(self.pred_model_obj.name))
        plt_path = "{}.png".format(get_folder_path(self.pred_model_obj, 'confusion_matrix'))
        plt.savefig(settings.MEDIA_ROOT + '/' + plt_path)
        self.pred_model_obj.confusion_matrix = plt_path
        plt.close()

        # Classification Report
        self.pred_model_obj.classification_report = classification_report(self.y_test, y_pred, digits=3)

        # PRC Plot
        plot_precision_recall_curve(self.loaded_clf, self.X_test, self.y_test, name=self.pred_model_obj.name)
        plt.ylim(0, 1)
        plt_path = "{}.png".format(get_folder_path(self.pred_model_obj, 'prc_plot'))
        plt.savefig(settings.MEDIA_ROOT + '/' + plt_path)
        self.pred_model_obj.prc_plot = plt_path
        plt.close()

        # ROC Plot
        plot_roc_curve(self.loaded_clf, self.X_test, self.y_test, name=self.pred_model_obj.name)
        plt.ylim(0, 1)
        plt_path = "{}.png".format(get_folder_path(self.pred_model_obj, 'roc_plot'))
        plt.savefig(settings.MEDIA_ROOT + '/' + plt_path)
        self.pred_model_obj.roc_plot = plt_path
        plt.close()

        # Top 5 important features
        top_n = 5
        feature_imp_map = {}
        for idx, name in enumerate(self.feature_labels):
            feature_imp_map[name] = self.loaded_clf.feature_importances_[idx]
        feature_imp_map = {k: v for k, v in sorted(feature_imp_map.items(), key=lambda item: item[1], reverse=True)}
        plt.bar(range(top_n), list(feature_imp_map.values())[:top_n])
        plt.xticks(range(top_n), list(feature_imp_map.keys())[:top_n], rotation='vertical')
        plt.title('Top {} Features'.format(top_n))
        plt.ylabel('Importance')
        plt.xlabel('Features')
        plt.ylim(0, 1)
        plt_path = "{}.png".format(get_folder_path(self.pred_model_obj, 'feature_importance'))
        plt.savefig(settings.MEDIA_ROOT + '/' + plt_path)
        self.pred_model_obj.feature_importance_plot = plt_path
        plt.close()

        # Best feature boxplot
        top_feature_label = list(feature_imp_map.keys())[0]
        top_feature_idx = self.feature_labels.index(top_feature_label)
        values_0 = []
        values_1 = []
        for idx, y_val in enumerate(self.y_train):
            if y_val == 0:
                values_0.append(self.X_train[idx][top_feature_idx])
            else:
                values_1.append(self.X_train[idx][top_feature_idx])
        fig, ax = plt.subplots()
        boxplt = ax.boxplot([values_0, values_1], patch_artist=True, notch=True)
        for patch, color in zip(boxplt['boxes'], ['#176D9C', '#C38820']):
            patch.set_facecolor(color)
        ax.set_xticklabels([0, 1])
        plt.ylim(0, 1)
        plt.ylabel(top_feature_label)
        plt.title('Distinguishing power of the best feature')
        plt_path = "{}.png".format(get_folder_path(self.pred_model_obj, 'best_feature_box_plot'))
        plt.savefig(settings.MEDIA_ROOT + '/' + plt_path)
        self.pred_model_obj.best_feature_box_plot = plt_path
        plt.close()

        # Update report in database entry
        self.pred_model_obj.save()
