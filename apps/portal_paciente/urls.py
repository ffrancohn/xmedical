from django.urls import path

from .views import (
    PortalCitasView,
    PortalDashboardView,
    PortalHistoriaView,
    PortalRegistroView,
    PortalSolicitarCitaView,
    portal_cancelar_cita,
    portal_exportar_hce,
    portal_llegada_cita,
)

urlpatterns = [
    path("", PortalDashboardView.as_view(), name="portal_dashboard"),
    path("registro/", PortalRegistroView.as_view(), name="portal_registro"),
    path("citas/", PortalCitasView.as_view(), name="portal_citas"),
    path("citas/solicitar/", PortalSolicitarCitaView.as_view(), name="portal_solicitar_cita"),
    path("citas/<int:pk>/cancelar/", portal_cancelar_cita, name="portal_cancelar_cita"),
    path("citas/<int:pk>/llegada/", portal_llegada_cita, name="portal_llegada_cita"),
    path("historia/", PortalHistoriaView.as_view(), name="portal_historia"),
    path("historia/exportar/<str:formato>/", portal_exportar_hce, name="portal_exportar_hce"),
]
