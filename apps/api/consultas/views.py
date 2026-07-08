from django.utils import timezone
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated

from apps.api.mixins import InstitucionScopedMixin
from apps.api.permissions import IsMedicoAPI
from apps.consulta.models import Consulta

from .serializers import ConsultaCreateSerializer, ConsultaSerializer


class ConsultaViewSet(InstitucionScopedMixin, viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsMedicoAPI]
    http_method_names = ["get", "post", "patch", "head", "options"]

    def get_serializer_class(self):
        if self.action == "create":
            return ConsultaCreateSerializer
        return ConsultaSerializer

    def get_queryset(self):
        qs = self.filter_by_institucion(
            Consulta.objects.select_related("cita__paciente", "cita__profesional")
        )
        if self.request.query_params.get("hoy") == "1":
            qs = qs.filter(cita__fecha=timezone.localdate())
        return qs.order_by("-creado_en")

    def perform_create(self, serializer):
        cita = serializer.validated_data["cita"]
        institucion = self.get_institucion()
        if cita.institucion_id != institucion.id:
            raise PermissionDenied("La cita no pertenece a su institucion.")
        serializer.save(institucion=institucion)
