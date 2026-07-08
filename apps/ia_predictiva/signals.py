from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.citas.models import Cita
from apps.preclinica.models import Preclinica

from .services import guardar_prediccion_ausentismo, sincronizar_alertas_riesgo


@receiver(post_save, sender=Cita)
def actualizar_prediccion_cita(sender, instance, **kwargs):
    guardar_prediccion_ausentismo(instance)


@receiver(post_save, sender=Preclinica)
def actualizar_riesgo_preclinica(sender, instance, **kwargs):
    paciente = instance.cita.paciente
    sincronizar_alertas_riesgo(
        paciente=paciente,
        institucion=instance.institucion,
        preclinica=instance,
        cita=instance.cita,
    )
