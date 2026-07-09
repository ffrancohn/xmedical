from django.urls import path

from .views import (
    AdministracionDashboardView,
    EnfermeriaDashboardView,
    EpidemiologiaDashboardView,
    EspecialistaDashboardView,
)

urlpatterns = [
    path("enfermeria/", EnfermeriaDashboardView.as_view(), name="dashboards_enfermeria"),
    path("administracion/", AdministracionDashboardView.as_view(), name="dashboards_administracion"),
    path("especialista/", EspecialistaDashboardView.as_view(), name="dashboards_especialista"),
    path("epidemiologia/", EpidemiologiaDashboardView.as_view(), name="dashboards_epidemiologia"),
]
