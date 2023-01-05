from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from pred_models.forms import PredModelForm
from pred_models.models import PredModel
from pred_models.metrics import generate


@login_required(login_url='login')
def pred_model_upload(request):
    if request.method == "GET":
        return render(
            request, 'pred_models/model_upload_form.html',
            {'form': PredModelForm}
        )
    elif request.method == "POST":
        form = PredModelForm(request.POST, request.FILES)
        upload_resp = form.is_valid()
        if upload_resp:
            try:
                pred_model = form.save(commit=False)
                pred_model.developer = request.user
                pred_model.save()
            except Exception as e:
                upload_resp = False
                print(str(e))
        return render(
            request, 'pred_models/model_upload_done.html',
            {'upload_resp': upload_resp}
        )


@login_required(login_url='login')
def pred_models_list(request):
    pred_models = PredModel.objects.filter(developer=request.user)
    return render(
        request, 'pred_models/list.html',
        {'pred_models': pred_models}
    )


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
        pred_model = generate(pred_model)
    except ValueError:
        message = 'Model train test failed'
    return render(
        request, 'pred_models/view.html',
        {
            'pred_model': pred_model,
            'pred_model_id': pred_model_id,
            'message': message
        }
    )
