from django.urls import path

from .views import PacienteCreateView, PacienteDetailView, PacienteListView, PacienteUpdateView, paciente_historia_redirect

urlpatterns = [
    path("", PacienteListView.as_view(), name="pacientes_lista"),
    path("nuevo/", PacienteCreateView.as_view(), name="pacientes_nuevo"),
    path("<int:pk>/", PacienteDetailView.as_view(), name="pacientes_detalle"),
    path("<int:pk>/editar/", PacienteUpdateView.as_view(), name="pacientes_editar"),
    path("<int:pk>/historia/", paciente_historia_redirect, name="pacientes_historia"),
]
