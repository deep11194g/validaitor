from django.db import models


class PredModel(models.Model):
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField('date published')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)