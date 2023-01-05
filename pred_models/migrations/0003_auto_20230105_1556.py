# Generated by Django 3.2.16 on 2023-01-05 15:56

from django.db import migrations, models
import pred_models.models


class Migration(migrations.Migration):

    dependencies = [
        ('pred_models', '0002_auto_20230104_1058'),
    ]

    operations = [
        migrations.AddField(
            model_name='predmodel',
            name='best_feature_box_plot',
            field=models.ImageField(max_length=500, null=True, upload_to=pred_models.models.get_folder_path),
        ),
        migrations.AlterField(
            model_name='predmodel',
            name='confusion_matrix',
            field=models.ImageField(max_length=500, null=True, upload_to=pred_models.models.get_folder_path),
        ),
        migrations.AlterField(
            model_name='predmodel',
            name='feature_importance_plot',
            field=models.ImageField(max_length=500, null=True, upload_to=pred_models.models.get_folder_path),
        ),
        migrations.AlterField(
            model_name='predmodel',
            name='prc_plot',
            field=models.ImageField(max_length=500, null=True, upload_to=pred_models.models.get_folder_path),
        ),
        migrations.AlterField(
            model_name='predmodel',
            name='roc_plot',
            field=models.ImageField(max_length=500, null=True, upload_to=pred_models.models.get_folder_path),
        ),
        migrations.AlterField(
            model_name='predmodel',
            name='test_set',
            field=models.FileField(max_length=500, upload_to=pred_models.models.get_folder_path),
        ),
        migrations.AlterField(
            model_name='predmodel',
            name='train_set',
            field=models.FileField(max_length=500, upload_to=pred_models.models.get_folder_path),
        ),
        migrations.AlterField(
            model_name='predmodel',
            name='trained_model',
            field=models.FileField(max_length=500, upload_to=pred_models.models.get_folder_path),
        ),
    ]