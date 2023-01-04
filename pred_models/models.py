from django.db import models
from django.contrib.auth.models import User


class PredModel(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=255, blank=True)
    trained_model = models.FileField(upload_to='trained_models/')
    train_set = models.FileField(upload_to='train_sets/')
    test_set = models.FileField(upload_to='test_sets/')
    developer = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
