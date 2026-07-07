from django.urls import path

from .views import ConsultaWizardView, cie10_search, historia_clinica, sugerir_diagnostico, wizard_autosave

urlpatterns = [
    path("cita/<int:cita_id>/paso/<int:step>/", ConsultaWizardView.as_view(), name="consulta_wizard"),
    path("cita/<int:cita_id>/autosave/", wizard_autosave, name="consulta_wizard_autosave"),
    path("cita/<int:cita_id>/sugerir-diagnostico/", sugerir_diagnostico, name="consulta_sugerir_diagnostico"),
    path("cie10/", cie10_search, name="cie10_search"),
    path("historia/<int:paciente_id>/", historia_clinica, name="historia_clinica"),
]
