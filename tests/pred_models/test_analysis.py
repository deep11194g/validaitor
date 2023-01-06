import os.path
import unittest

import numpy as np

from django.conf import settings
from django.contrib.auth.models import User
from pred_models.models import PredModel
from pred_models.analysis import csv_to_dataset, PerformanceStatsAnalyser


class TestAnalysis(unittest.TestCase):
    def setUp(self):
        self.test_user = User.objects.create(
            username='test',
            email='test@test.com',
            password='TestPass'
        )
        self.pred_model = PredModel.objects.create(
            name='test_model',
            description='test model for test purpose',
            trained_model=settings.MEDIA_ROOT + '/user_1/titanic_GBC/GradientBoostingClassifier__titanic_train_csv.pkl',
            test_set=settings.MEDIA_ROOT + '/user_1/titanic_GBC/titanic_test.csv',
            train_set=settings.MEDIA_ROOT + '/user_1/titanic_GBC/titanic_train.csv',
            developer=self.test_user
        )

    def tearDown(self):
        self.test_user.delete()
        self.pred_model.delete()

    def test_csv_to_dataset(self):
        X_train, y_train, labels = csv_to_dataset(csv_file_path=self.pred_model.train_set.path)
        self.assertIsInstance(X_train, np.ndarray)
        self.assertIsInstance(y_train, np.ndarray)
        self.assertEqual(2, X_train.ndim)
        self.assertEqual(1, y_train.ndim)
        self.assertIsInstance(labels, list)
        self.assertIsInstance(labels[0], str)
        self.assertEqual(len(labels), len(X_train[0]))

    def test_load(self):
        analyser = PerformanceStatsAnalyser(pred_model_obj=self.pred_model)
        self.assertIsNone(analyser.X_test)
        self.assertIsNone(analyser.X_train)
        self.assertIsNone(analyser.y_test)
        self.assertIsNone(analyser.y_test)
        self.assertIsNone(analyser.loaded_clf)
        analyser.load()
        self.assertIsNotNone(analyser.X_test)
        self.assertIsNotNone(analyser.X_train)
        self.assertIsNotNone(analyser.y_test)
        self.assertIsNotNone(analyser.y_test)
        self.assertIsNotNone(analyser.loaded_clf)

    def test__test_performance(self):
        analyser = PerformanceStatsAnalyser(pred_model_obj=self.pred_model)
        analyser.load()
        analyser.test_performance()
        self.assertIsNotNone(analyser.pred_model_obj.confusion_matrix)
        self.assertTrue(os.path.exists(analyser.pred_model_obj.confusion_matrix.path))
        self.assertIsNotNone(analyser.pred_model_obj.classification_report)
        self.assertIsInstance(analyser.pred_model_obj.classification_report, str)


if __name__ == '__main__':
    unittest.main()
