from django.urls import path

from .views import AdministracionDashboardView, EnfermeriaDashboardView, EspecialistaDashboardView

urlpatterns = [
    path("enfermeria/", EnfermeriaDashboardView.as_view(), name="dashboards_enfermeria"),
    path("administracion/", AdministracionDashboardView.as_view(), name="dashboards_administracion"),
    path("especialista/", EspecialistaDashboardView.as_view(), name="dashboards_especialista"),
]
