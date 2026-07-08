from rest_framework import serializers

from apps.preclinica.models import Preclinica


class PreclinicaSerializer(serializers.ModelSerializer):
    cita_id = serializers.IntegerField(source="cita.id", read_only=True)
    paciente = serializers.CharField(source="cita.paciente.__str__", read_only=True)

    class Meta:
        model = Preclinica
        fields = [
            "id",
            "cita",
            "cita_id",
            "paciente",
            "presion_arterial_sis",
            "presion_arterial_dia",
            "frecuencia_cardiaca",
            "temperatura",
            "saturacion_o2",
            "peso",
            "talla",
            "imc",
            "motivo_consulta",
            "triaje",
            "creado_en",
        ]
        read_only_fields = ["id", "creado_en", "imc"]


class PreclinicaCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Preclinica
        fields = [
            "cita",
            "presion_arterial_sis",
            "presion_arterial_dia",
            "frecuencia_cardiaca",
            "temperatura",
            "saturacion_o2",
            "peso",
            "talla",
            "motivo_consulta",
            "triaje",
        ]
