from functools import wraps

from django.contrib import messages
from django.shortcuts import redirect

from .models import Profesional


def get_profesional(user):
    if not user.is_authenticated or user.is_superuser:
        return None
    return Profesional.objects.filter(usuario=user, activo=True).select_related("institucion").first()


def role_required(*roles):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)
            profesional = get_profesional(request.user)
            if profesional and profesional.tipo in roles:
                return view_func(request, *args, **kwargs)
            messages.error(request, "No tienes permiso para acceder a esta seccion.")
            return redirect("dashboard")

        return wrapper

    return decorator
