from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.api.mixins import InstitucionScopedMixin
from apps.api.permissions import IsClinicalStaffAPI, IsRecepcionistaAPI
from apps.citas.models import Cita

from .serializers import CitaSerializer, CitaUpdateSerializer


class CitaViewSet(InstitucionScopedMixin, viewsets.ModelViewSet):
    http_method_names = ["get", "post", "patch", "head", "options"]

    def get_permissions(self):
        if self.action == "create":
            return [IsAuthenticated(), IsRecepcionistaAPI()]
        if self.action in ("partial_update", "update"):
            return [IsAuthenticated(), IsRecepcionistaAPI()]
        return [IsAuthenticated(), IsClinicalStaffAPI()]

    def get_serializer_class(self):
        if self.action in ("partial_update", "update"):
            return CitaUpdateSerializer
        return CitaSerializer

    def get_queryset(self):
        qs = self.filter_by_institucion(
            Cita.objects.select_related("paciente", "profesional")
        )
        fecha = self.request.query_params.get("fecha")
        if fecha:
            qs = qs.filter(fecha=fecha)
        estado = self.request.query_params.get("estado")
        if estado:
            qs = qs.filter(estado=estado)
        return qs.order_by("fecha", "hora")

    def perform_create(self, serializer):
        serializer.save(institucion=self.get_institucion(), tipo_agendamiento="especifico")
