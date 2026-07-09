from django.urls import path

from .views import QRGenerarView, qr_lista_consulta, qr_mostrar, qr_validar

urlpatterns = [
    path("validar/<str:token>/", qr_validar, name="qr_validar"),
    path("mostrar/<str:token>/", qr_mostrar, name="qr_mostrar"),
    path("consulta/<int:consulta_id>/", qr_lista_consulta, name="qr_lista_consulta"),
    path("generar/<int:consulta_id>/<str:tipo>/", QRGenerarView.as_view(), name="qr_generar"),
]
