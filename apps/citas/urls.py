from django.urls import path

from .views import CitaCreateView, CitaListView, cancelar_cita

urlpatterns = [
    path("", CitaListView.as_view(), name="citas_lista"),
    path("agendar/", CitaCreateView.as_view(), name="citas_agendar"),
    path("<int:pk>/cancelar/", cancelar_cita, name="citas_cancelar"),
]
