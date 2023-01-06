from django.urls import path
from pred_models import views

urlpatterns = [
    path('', views.pred_models_list, name='pred_models_list'),
    path('<int:pred_model_id>', views.pred_model_detail, name='pred_model_detail'),
    path('upload', views.pred_model_upload, name='pred_model_upload'),
    path('<int:pred_model_id>/generate_report', views.generate_report, name='generate_report'),
    path('<int:pred_model_id>/download_report', views.generate_report, name='download_report')
]
