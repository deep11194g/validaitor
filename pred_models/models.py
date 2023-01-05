from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.contrib.auth.models import User


def get_folder_path(instance, filename):
    return 'user_{}/{}/{}'.format(instance.developer.id, instance.name, filename)


class PredModel(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=255, blank=True)
    trained_model = models.FileField(upload_to=get_folder_path, max_length=500)
    train_set = models.FileField(upload_to=get_folder_path, max_length=500)
    test_set = models.FileField(upload_to=get_folder_path, max_length=500)

    features = ArrayField(models.CharField(max_length=80), null=True)
    confusion_matrix = models.ImageField(upload_to=get_folder_path, null=True, max_length=500)
    classification_report = models.TextField(null=True)
    prc_plot = models.ImageField(upload_to=get_folder_path, null=True, max_length=500)
    roc_plot = models.ImageField(upload_to=get_folder_path, null=True, max_length=500)
    feature_importance_plot = models.ImageField(upload_to=get_folder_path, null=True, max_length=500)
    best_feature_box_plot = models.ImageField(upload_to=get_folder_path, null=True, max_length=500)

    developer = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
