from django import forms

from pred_models.models import PredModel


class PredModelForm(forms.ModelForm):
    class Meta:
        model = PredModel
        fields = ('name', 'description', 'trained_model', 'train_set', 'test_set')
