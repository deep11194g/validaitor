import sys, os

sys.path.append(os.environ.get('SRC_DIR'))

import pickle

from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, GradientBoostingClassifier, \
    ExtraTreesClassifier
from sklearn.svm import SVC

from django.conf import settings
from pred_models.analysis import csv_to_dataset


def generate_pickle(model_cls, train_data_csv_file):
    X_train, y_train, _ = csv_to_dataset(train_data_csv_file)
    model_obj = model_cls()
    model_obj.fit(X_train, y_train)
    data_file_name = train_data_csv_file.split('/')[-1].replace('.', '_')
    pkl_file_path = "{}/test_model/{}__{}.pkl".format(settings.MEDIA_ROOT, model_cls.__name__, data_file_name)
    pickle.dump(model_obj, open(pkl_file_path, 'wb'))
    print("Generated {}".format(pkl_file_path))


if __name__ == '__main__':
    train_data_file = settings.MEDIA_ROOT + '/user_1/titanic/titanic_train.csv'
    for cls in [RandomForestClassifier, AdaBoostClassifier, GradientBoostingClassifier, ExtraTreesClassifier,
                SVC]:
        generate_pickle(cls, train_data_file)
