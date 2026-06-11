from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include("apps.auth_app.urls")),
    path("pacientes/", include("apps.pacientes.urls")),
    path("citas/", include("apps.citas.urls")),
    path("preclinica/", include("apps.preclinica.urls")),
    path("consulta/", include("apps.consulta.urls")),
    path("referencias/", include("apps.referencias.urls")),
    path("qr/", include("apps.qr.urls")),
    path("", include("apps.core.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
