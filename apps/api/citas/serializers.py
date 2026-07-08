from rest_framework import serializers

from apps.citas.models import Cita


class CitaSerializer(serializers.ModelSerializer):
    paciente_nombre = serializers.CharField(source="paciente.__str__", read_only=True)
    profesional_nombre = serializers.CharField(source="profesional.nombre", read_only=True)

    class Meta:
        model = Cita
        fields = [
            "id",
            "paciente",
            "paciente_nombre",
            "profesional",
            "profesional_nombre",
            "fecha",
            "hora",
            "estado",
            "tipo_agendamiento",
            "creado_en",
        ]
        read_only_fields = ["id", "creado_en", "tipo_agendamiento"]


class CitaUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cita
        fields = ["estado", "fecha", "hora"]
