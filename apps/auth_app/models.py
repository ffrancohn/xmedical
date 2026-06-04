from django.conf import settings
from django.db import models


class UserPreference(models.Model):
    THEME_CHOICES = [
        ("garden", "Garden"),
        ("light", "Claro"),
        ("dark", "Oscuro"),
        ("corporate", "Corporativo"),
        ("emerald", "Esmeralda"),
        ("cupcake", "Suave"),
        ("bumblebee", "Amarillo"),
        ("winter", "Invierno"),
        ("night", "Noche"),
        ("forest", "Bosque"),
        ("aqua", "Aqua"),
        ("lofi", "Minimalista"),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="preference")
    theme = models.CharField(max_length=30, choices=THEME_CHOICES, default="garden")
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Preferencias de {self.user.username}"
