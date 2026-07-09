from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from apps.core.models import Profesional
from apps.portal_paciente.models import PerfilPaciente


class XMedicalTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        profesional = Profesional.objects.filter(usuario=user, activo=True).select_related("institucion").first()
        if profesional:
            data["institucion_id"] = profesional.institucion_id
            data["institucion_nombre"] = profesional.institucion.nombre
            data["rol"] = profesional.tipo
            data["profesional_id"] = profesional.id
        elif user.is_superuser:
            data["institucion_id"] = None
            data["institucion_nombre"] = None
            data["rol"] = "superadmin"
            data["profesional_id"] = None
        else:
            perfil = PerfilPaciente.objects.filter(usuario=user, activo=True).select_related("institucion").first()
            if not perfil:
                raise serializers.ValidationError("Usuario sin rol clinico o portal asignado.")
            data["institucion_id"] = perfil.institucion_id
            data["institucion_nombre"] = perfil.institucion.nombre
            data["rol"] = "paciente"
            data["profesional_id"] = None
            data["paciente_id"] = perfil.paciente_id
        data["user_id"] = user.id
        data["username"] = user.username
        return data

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        profesional = Profesional.objects.filter(usuario=user, activo=True).first()
        if profesional:
            token["institucion_id"] = profesional.institucion_id
            token["rol"] = profesional.tipo
        elif user.is_superuser:
            token["institucion_id"] = None
            token["rol"] = "superadmin"
        else:
            perfil = PerfilPaciente.objects.filter(usuario=user, activo=True).first()
            if perfil:
                token["institucion_id"] = perfil.institucion_id
                token["rol"] = "paciente"
        token["user_id"] = user.id
        return token


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()
