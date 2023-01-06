from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

from users.views import home, register

urlpatterns = [
    path('', home, name="home"),
    path('accounts/', include("django.contrib.auth.urls")),
    path('register/', register, name="register"),
    path('pred_models/', include('pred_models.urls')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
