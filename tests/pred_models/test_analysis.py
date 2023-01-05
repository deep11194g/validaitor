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


if __name__ == '__main__':
    unittest.main()
