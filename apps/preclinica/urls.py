from django.urls import path

from .views import PreclinicaListView, PreclinicaRegistroView

urlpatterns = [
    path("", PreclinicaListView.as_view(), name="preclinica_lista"),
    path("<int:cita_id>/", PreclinicaRegistroView.as_view(), name="preclinica_registro"),
]
