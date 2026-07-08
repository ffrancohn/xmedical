from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.api.mixins import InstitucionScopedMixin
from apps.api.permissions import IsMedicoAPI
from apps.citas.models import Cita
from apps.consulta.models import Consulta
from apps.pacientes.models import Paciente


class DashboardView(InstitucionScopedMixin, APIView):
    permission_classes = [IsAuthenticated, IsMedicoAPI]

    def get(self, request):
        institucion = self.get_institucion()
        hoy = timezone.localdate()
        citas_hoy = Cita.objects.filter(institucion=institucion, fecha=hoy)
        return Response(
            {
                "fecha": hoy,
                "institucion_id": institucion.id,
                "institucion_nombre": institucion.nombre,
                "citas_total": citas_hoy.count(),
                "citas_pendientes": citas_hoy.filter(estado__in=["pendiente", "confirmada", "en_espera"]).count(),
                "citas_atendidas": citas_hoy.filter(estado="atendida").count(),
                "pacientes_activos": Paciente.objects.filter(institucion=institucion, activo=True).count(),
                "consultas_hoy": Consulta.objects.filter(institucion=institucion, cita__fecha=hoy).count(),
            }
        )
