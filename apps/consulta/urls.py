from django.urls import path

from .views import ConsultaWizardView, cie10_search, historia_clinica

urlpatterns = [
    path("cita/<int:cita_id>/paso/<int:step>/", ConsultaWizardView.as_view(), name="consulta_wizard"),
    path("cie10/", cie10_search, name="cie10_search"),
    path("historia/<int:paciente_id>/", historia_clinica, name="historia_clinica"),
]
