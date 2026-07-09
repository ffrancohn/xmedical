from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.api.mixins import InstitucionScopedMixin
from apps.api.permissions import IsEnfermeraAPI
from apps.citas.models import Cita
from apps.preclinica.models import Preclinica

from .serializers import PreclinicaCreateSerializer, PreclinicaSerializer


class PreclinicaViewSet(InstitucionScopedMixin, viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsEnfermeraAPI]
    http_method_names = ["get", "post", "head", "options"]

    def get_serializer_class(self):
        if self.action == "create":
            return PreclinicaCreateSerializer
        return PreclinicaSerializer

    def get_queryset(self):
        return self.filter_by_institucion(
            Preclinica.objects.select_related("cita__paciente")
        ).order_by("-creado_en")

    def perform_create(self, serializer):
        cita = serializer.validated_data["cita"]
        institucion = self.get_institucion()
        if cita.institucion_id != institucion.id:
            raise PermissionDenied("La cita no pertenece a su institucion.")
        preclinica = serializer.save(institucion=institucion)
        cita.estado = "en_espera"
        cita.save(update_fields=["estado"])
        return preclinica

    @action(detail=False, methods=["get"], url_path="pendientes")
    def pendientes(self, request):
        institucion = self.get_institucion()
        citas = Cita.objects.filter(
            institucion=institucion,
            fecha=timezone.localdate(),
            estado__in=["pendiente", "confirmada"],
        ).select_related("paciente", "profesional")
        citas = citas.exclude(pk__in=Preclinica.objects.filter(cita__in=citas).values_list("cita_id", flat=True))
        data = [
            {
                "id": c.id,
                "paciente": str(c.paciente),
                "profesional": c.profesional.nombre,
                "fecha": c.fecha,
                "hora": c.hora,
                "estado": c.estado,
            }
            for c in citas.order_by("hora")
        ]
        return Response(data, status=status.HTTP_200_OK)
