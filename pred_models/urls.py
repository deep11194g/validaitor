from django.urls import path
from pred_models.views import pred_model_upload, pred_models_list, pred_model_detail

urlpatterns = [
    path('', pred_models_list, name='pred_models_list'),
    path('<int:pred_model_id>/', pred_model_detail, name='pred_model_detail'),
    path('/upload', pred_model_upload, name='pred_model_upload'),

]
