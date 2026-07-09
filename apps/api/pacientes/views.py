from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.api.mixins import InstitucionScopedMixin
from apps.api.permissions import IsClinicalStaffAPI, IsRecepcionistaAPI
from apps.pacientes.models import Paciente

from .serializers import PacienteSerializer


class PacienteViewSet(InstitucionScopedMixin, viewsets.ModelViewSet):
    serializer_class = PacienteSerializer

    def get_permissions(self):
        if self.action in ("create", "update", "partial_update"):
            return [IsAuthenticated(), IsRecepcionistaAPI()]
        return [IsAuthenticated(), IsClinicalStaffAPI()]

    def get_queryset(self):
        return self.filter_by_institucion(Paciente.objects.filter(activo=True)).order_by("apellido", "nombre")

    def perform_create(self, serializer):
        serializer.save(institucion=self.get_institucion())
