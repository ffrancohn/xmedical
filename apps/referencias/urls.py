from django.urls import path

from .views import (
    ContrarreferenciaCreateView,
    ReferenciaAgendarView,
    ReferenciaAceptarView,
    ReferenciaCreateView,
    ReferenciaDetailView,
    ReferenciaListView,
    ReferenciaRechazarView,
)

urlpatterns = [
    path("", ReferenciaListView.as_view(), name="referencias_lista"),
    path("nueva/<int:consulta_id>/", ReferenciaCreateView.as_view(), name="referencias_nueva"),
    path("<int:pk>/", ReferenciaDetailView.as_view(), name="referencias_detalle"),
    path("<int:pk>/aceptar/", ReferenciaAceptarView.as_view(), name="referencias_aceptar"),
    path("<int:pk>/rechazar/", ReferenciaRechazarView.as_view(), name="referencias_rechazar"),
    path("<int:pk>/agendar/", ReferenciaAgendarView.as_view(), name="referencias_agendar"),
    path("<int:pk>/contrarreferencia/", ContrarreferenciaCreateView.as_view(), name="referencias_contrarreferencia"),
]
