import traceback

from fpdf import FPDF
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.conf import settings

from pred_models.forms import PredModelForm
from pred_models.models import PredModel, get_folder_path
from pred_models.analysis import PerformanceStatsAnalyser

from django.http import HttpResponse


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
            'text': 'Error in model test metric generation'
        }
    return render(
        request, 'pred_models/view.html',
        {
            'pred_model': pred_model,
            'pred_model_id': pred_model_id,
            'message': message
        }
    )


@login_required(login_url='login')
def download_report(request, pred_model_id):
    # TODO: Not working yet
    pred_model = PredModel.objects.get(pk=pred_model_id)
    message = None
    if pred_model.developer != request.user:
        pred_model = None

    if not pred_model:
        message = {
            'color': 'red',
            'text': 'Pred model with ID {} doesnt exists or belong to you'.format(pred_model_id)
        }
    if not (pred_model.confusion_matrix or pred_model.classification_report or pred_model.roc_plot
            or pred_model.prc_plot):
        message = {
            'color': 'red',
            'text': 'Report for Pred model with ID {} has not been generated yet'.format(pred_model_id)
        }
    if message:
        return render(
            request, 'pred_models/view.html',
            {
                'pred_model': pred_model,
                'pred_model_id': pred_model_id,
                'message': message
            }
        )

    # Generate PDF and store in the directory as other model files
    pdf = FPDF()
    for image_file in [pred_model.confusion_matrix.path, pred_model.classification_report.partition(),
                       pred_model.roc_plot.path, pred_model.prc_plot.path]:
        pdf.add_page()
        pdf.image(image_file)
    pdf_store_path = settings.MEDIA_ROOT + '/'+ get_folder_path(pred_model, 'performance_report.pdf')
    pdf.output(pdf_store_path, "F")

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(pdf_store_path)
    return response
