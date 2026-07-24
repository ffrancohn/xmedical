from django.urls import path

from .views import PreferenciasVisualesView, PortalLoginView, RegistroProfesionalView, XMedicalLoginView, XMedicalLogoutView

urlpatterns = [
    path("login/", XMedicalLoginView.as_view(), name="login"),
    path("login/paciente/", PortalLoginView.as_view(), name="login_paciente"),
    path("logout/", XMedicalLogoutView.as_view(), name="logout"),
    path("registro/", RegistroProfesionalView.as_view(), name="registro_profesional"),
    path("preferencias/", PreferenciasVisualesView.as_view(), name="preferencias_visuales"),
]
