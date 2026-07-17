from django.conf import settings
from django.db import models


class UserPreference(models.Model):
    THEME_CHOICES = [
        ("vital", "Vital"),
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
    theme = models.CharField(max_length=30, choices=THEME_CHOICES, default="vital")
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Preferencias de {self.user.username}"
