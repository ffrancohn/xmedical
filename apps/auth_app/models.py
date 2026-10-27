from django.conf import settings
from django.db import models


class UserPreference(models.Model):
    INTERFACE_CHOICES = [
        ("classic", "Clásica (sidebar DaisyUI)"),
        ("atlas", "Atlas (isométrica, estilo prototipo)"),
    ]

    THEME_CHOICES = [
        ("garden", "Garden"),
        ("emerald", "Esmeralda"),
        ("aqua", "Aqua"),
        ("corporate", "Corporativo"),
        ("light", "Claro"),
        ("dark", "Oscuro"),
        ("cupcake", "Suave"),
        ("bumblebee", "Amarillo"),
        ("winter", "Invierno"),
        ("night", "Noche"),
        ("forest", "Bosque"),
        ("lofi", "Minimalista"),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="preference")
    theme = models.CharField(max_length=30, choices=THEME_CHOICES, default="garden")
    interface_mode = models.CharField(max_length=20, choices=INTERFACE_CHOICES, default="classic")
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Preferencias de {self.user.username}"
