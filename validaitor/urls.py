from django.conf.urls import url
from django.urls import include, path
from django.contrib import admin

urlpatterns = [
    url(r"^admin/", admin.site.urls),
    url(r"^", include("users.urls")),
    path('pred_models/', include('pred_models.urls')),
]
