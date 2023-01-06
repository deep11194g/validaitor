import traceback

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, reverse

from pred_models.forms import PredModelForm
from pred_models.models import PredModel
from pred_models.analysis import PerformanceStatsAnalyser


@login_required(login_url='login')
def pred_model_upload(request):
    if request.method == "GET":
        return render(
            request, 'pred_models/model_upload_form.html',
            {'form': PredModelForm}
        )

    elif request.method == "POST":
        form = PredModelForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                pred_model = form.save(commit=False)
                pred_model.developer = request.user
                pred_model.save()
                return _list(request=request, message={
                    'color': 'green',
                    'text': 'New model uploaded with ID: {}'.format(pred_model.id)
                })
            except Exception as e:
                print(str(e))
        return render(
            request, 'pred_models/model_upload_form.html',
            {
                'form': PredModelForm,
                'message': {
                    'color': 'red',
                    'text': 'Model upload failed, you may retry !!!'
                }
            }
        )


def _list(request, message=None):
    kwargs = {'pred_models': PredModel.objects.filter(developer=request.user).order_by('-id')}
    if message:
        kwargs['message'] = message
    return render(request, 'pred_models/list.html', kwargs)


@login_required(login_url='login')
def pred_models_list(request):
    return _list(request)


@login_required(login_url='login')
def pred_model_detail(request, pred_model_id):
    pred_model = PredModel.objects.get(pk=pred_model_id)
    if pred_model.developer != request.user:
        pred_model = None
    return render(
        request, 'pred_models/view.html',
        {
            'pred_model': pred_model,
            'pred_model_id': pred_model_id
        }
    )


@login_required(login_url='login')
def generate_report(request, pred_model_id):
    pred_model = PredModel.objects.get(pk=pred_model_id)
    message = None
    if pred_model.developer != request.user:
        pred_model = None
    try:
        analyser = PerformanceStatsAnalyser(pred_model_obj=pred_model)
        analyser.load()
        analyser.test_performance()
        pred_model = analyser.pred_model_obj
    except Exception as e:
        print(str(e))
        print(traceback.format_exc())
        message = {
            'color': 'red',
            'text':'Error in model test metric generation'
        }
    return render(
        request, 'pred_models/view.html',
        {
            'pred_model': pred_model,
            'pred_model_id': pred_model_id,
            'message': message
        }
    )
