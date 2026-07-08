from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.core.models import Institucion


class XMedicalJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        result = super().authenticate(request)
        if result is None:
            return None
        user, validated_token = result
        institucion_id = validated_token.get("institucion_id")
        rol = validated_token.get("rol")
        request.api_rol = rol
        if institucion_id:
            request.institucion = Institucion.objects.filter(pk=institucion_id, activo=True).first()
        elif rol == "superadmin":
            request.institucion = None
        return user, validated_token
