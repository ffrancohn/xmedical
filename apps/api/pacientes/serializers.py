from rest_framework import serializers

from apps.pacientes.models import Paciente


class PacienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paciente
        fields = [
            "id",
            "documento",
            "nombre",
            "apellido",
            "fecha_nacimiento",
            "sexo",
            "telefono",
            "telefono_fijo",
            "email",
            "direccion",
            "ciudad",
            "departamento",
            "activo",
        ]
        read_only_fields = ["id"]
