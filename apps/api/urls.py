from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter

from apps.api.auth.views import LoginView, LogoutView, RefreshView
from apps.api.citas.views import CitaViewSet
from apps.api.consultas.views import ConsultaViewSet
from apps.api.dashboard.views import DashboardView
from apps.api.pacientes.views import PacienteViewSet
from apps.api.preclinica.views import PreclinicaViewSet

router = DefaultRouter()
router.register("pacientes", PacienteViewSet, basename="api-pacientes")
router.register("citas", CitaViewSet, basename="api-citas")
router.register("preclinica", PreclinicaViewSet, basename="api-preclinica")
router.register("consultas", ConsultaViewSet, basename="api-consultas")

urlpatterns = [
    path("auth/login/", LoginView.as_view(), name="api_login"),
    path("auth/refresh/", RefreshView.as_view(), name="api_refresh"),
    path("auth/logout/", LogoutView.as_view(), name="api_logout"),
    path("dashboard/", DashboardView.as_view(), name="api_dashboard"),
    path("schema/", SpectacularAPIView.as_view(), name="api_schema"),
    path("docs/", SpectacularSwaggerView.as_view(url_name="api_schema"), name="api_docs"),
    path("", include(router.urls)),
]
