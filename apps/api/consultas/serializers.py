from rest_framework import serializers

from apps.consulta.models import Consulta


class ConsultaSerializer(serializers.ModelSerializer):
    paciente = serializers.CharField(source="cita.paciente.__str__", read_only=True)
    cita_fecha = serializers.DateField(source="cita.fecha", read_only=True)
    cita_hora = serializers.TimeField(source="cita.hora", read_only=True)

    class Meta:
        model = Consulta
        fields = [
            "id",
            "cita",
            "paciente",
            "cita_fecha",
            "cita_hora",
            "motivo_consulta",
            "anamnesis",
            "examen_fisico",
            "plan_terapeutico",
            "conducta",
            "creado_en",
        ]
        read_only_fields = ["id", "creado_en"]


class ConsultaCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consulta
        fields = ["cita", "motivo_consulta", "anamnesis", "examen_fisico", "plan_terapeutico", "conducta"]
