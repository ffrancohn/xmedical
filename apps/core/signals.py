from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver

from apps.citas.models import Cita
from apps.consulta.models import Consulta, Diagnostico
from apps.pacientes.models import Paciente
from apps.preclinica.models import Preclinica

from .audit import AUDITED_MODELS, log_audit, serialize_instance

AUDITED_CLASSES = {Paciente, Cita, Preclinica, Consulta, Diagnostico}


@receiver(pre_save)
def capture_previous_values(sender, instance, **kwargs):
    if sender not in AUDITED_CLASSES or not instance.pk:
        return
    previous = sender.objects.filter(pk=instance.pk).first()
    if previous:
        instance._audit_previous = serialize_instance(previous)


@receiver(post_save)
def audit_save(sender, instance, created, **kwargs):
    if sender not in AUDITED_CLASSES:
        return
    if sender._meta.label not in AUDITED_MODELS:
        return
    if created:
        log_audit(instance, "CREATE", valor_nuevo=serialize_instance(instance))
        return
    previous = getattr(instance, "_audit_previous", None)
    current = serialize_instance(instance)
    if previous != current:
        log_audit(instance, "UPDATE", valor_anterior=previous, valor_nuevo=current)


@receiver(post_delete)
def audit_delete(sender, instance, **kwargs):
    if sender not in AUDITED_CLASSES:
        return
    log_audit(instance, "DELETE", valor_anterior=serialize_instance(instance))
