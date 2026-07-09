from django.apps import AppConfig


class IaPredictivaConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.ia_predictiva"
    verbose_name = "IA predictiva"

    def ready(self):
        from . import signals  # noqa: F401
