import json
from contextlib import contextmanager

from django.apps import apps
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core import serializers
from django.db import transaction
from django.utils import timezone
from django.utils.crypto import get_random_string

from apps.citas.models import Cita
from apps.consulta.models import Consulta, Diagnostico
from apps.core.models import BackupLog, Especialidad, Horario, Institucion, Profesional
from apps.ia_predictiva.models import AlertaRiesgoCronico, DemandaCita, PrediccionAusentismo
from apps.notificaciones.models import LogNotificacion, RecordatorioMedicamento
from apps.pacientes.models import DocumentoOCRLog, Paciente
from apps.portal_paciente.models import PerfilPaciente
from apps.preclinica.models import Preclinica
from apps.qr.models import DocumentoQR
from apps.referencias.models import Contrarreferencia, Referencia
from apps.variables_clinicas.models import ValorVariableClinica, VariableClinica

FORMAT_VERSION = 1


@contextmanager
def _mute_predictive_signals():
    from django.db.models.signals import post_save

    from apps.ia_predictiva.signals import actualizar_prediccion_cita, actualizar_riesgo_preclinica

    post_save.disconnect(actualizar_prediccion_cita, sender=Cita)
    post_save.disconnect(actualizar_riesgo_preclinica, sender=Preclinica)
    try:
        yield
    finally:
        post_save.connect(actualizar_prediccion_cita, sender=Cita)
        post_save.connect(actualizar_riesgo_preclinica, sender=Preclinica)


class TenantTransferError(Exception):
    pass


def _collect_users(institucion):
    user_ids = set(
        Profesional.objects.filter(institucion=institucion).values_list("usuario_id", flat=True)
    )
    user_ids.update(
        PerfilPaciente.objects.filter(institucion=institucion).values_list("usuario_id", flat=True)
    )
    user_ids.discard(None)
    return list(User.objects.filter(pk__in=user_ids))


def collect_tenant_objects(institucion):
    objects = []
    objects.extend(Institucion.objects.filter(pk=institucion.pk))
    objects.extend(Especialidad.objects.filter(institucion=institucion))
    objects.extend(_collect_users(institucion))
    objects.extend(Profesional.objects.filter(institucion=institucion))
    objects.extend(Horario.objects.filter(institucion=institucion))
    objects.extend(VariableClinica.objects.filter(institucion=institucion))
    objects.extend(Paciente.objects.filter(institucion=institucion))
    objects.extend(PerfilPaciente.objects.filter(institucion=institucion))
    objects.extend(Cita.objects.filter(institucion=institucion))
    objects.extend(Preclinica.objects.filter(institucion=institucion))
    objects.extend(Consulta.objects.filter(institucion=institucion))
    objects.extend(Diagnostico.objects.filter(institucion=institucion))
    objects.extend(ValorVariableClinica.objects.filter(institucion=institucion))
    objects.extend(Referencia.objects.filter(institucion=institucion))
    objects.extend(Contrarreferencia.objects.filter(institucion=institucion))
    objects.extend(DocumentoQR.objects.filter(institucion=institucion))
    objects.extend(RecordatorioMedicamento.objects.filter(institucion=institucion))
    objects.extend(LogNotificacion.objects.filter(institucion=institucion))
    objects.extend(PrediccionAusentismo.objects.filter(institucion=institucion))
    objects.extend(DemandaCita.objects.filter(institucion=institucion))
    objects.extend(AlertaRiesgoCronico.objects.filter(institucion=institucion))
    objects.extend(DocumentoOCRLog.objects.filter(institucion=institucion))
    return objects


def tenant_stats(institucion):
    return {
        "especialidades": Especialidad.objects.filter(institucion=institucion).count(),
        "profesionales": Profesional.objects.filter(institucion=institucion).count(),
        "pacientes": Paciente.objects.filter(institucion=institucion).count(),
        "citas": Cita.objects.filter(institucion=institucion).count(),
        "consultas": Consulta.objects.filter(institucion=institucion).count(),
        "referencias": Referencia.objects.filter(institucion=institucion).count(),
    }


def export_tenant_package(institucion):
    objects = collect_tenant_objects(institucion)
    serialized = json.loads(
        serializers.serialize(
            "json",
            objects,
            indent=2,
            use_natural_foreign_keys=False,
            use_natural_primary_keys=False,
        )
    )
    return {
        "format_version": FORMAT_VERSION,
        "exported_at": timezone.now().isoformat(),
        "source_institucion": {
            "id": institucion.id,
            "nombre": institucion.nombre,
            "subdominio": institucion.subdominio,
            "tipo": institucion.tipo,
        },
        "stats": tenant_stats(institucion),
        "records": serialized,
    }


def export_tenant_json(institucion):
    return json.dumps(export_tenant_package(institucion), ensure_ascii=False, indent=2)


def _unique_subdominio(base):
    candidate = base
    suffix = 1
    while Institucion.objects.filter(subdominio=candidate).exists():
        candidate = f"{base}-import-{suffix}"
        suffix += 1
    return candidate


def _unique_username(base):
    candidate = base
    suffix = 1
    while User.objects.filter(username=candidate).exists():
        candidate = f"{base}.import{suffix}"
        suffix += 1
    return candidate


def _remap_field(value, field, id_maps):
    if value is None:
        return None
    if not getattr(field, "many_to_one", False) and not getattr(field, "one_to_one", False):
        return value
    related_model = field.related_model
    model_label = related_model._meta.label_lower
    if model_label not in id_maps:
        return value
    return id_maps[model_label].get(value, value)


def _convert_field_value(field, value):
    if value is None:
        return None
    return field.to_python(value)


def _deserialize_record(record, id_maps):
    model = apps.get_model(record["model"])
    data = record["fields"].copy()
    create_data = {}
    for field in model._meta.fields:
        if field.name not in data:
            continue
        value = _remap_field(data[field.name], field, id_maps)
        if getattr(field, "many_to_one", False) or getattr(field, "one_to_one", False):
            create_data[f"{field.name}_id"] = value
        else:
            create_data[field.name] = _convert_field_value(field, value)
    if model._meta.label_lower == "auth.user":
        create_data.pop("password", None)
    obj = model.objects.create(**create_data)
    id_maps.setdefault(model._meta.label_lower, {})[record["pk"]] = obj.pk
    return obj


def import_tenant_package(
    package,
    *,
    mode="new",
    nombre=None,
    subdominio=None,
    target_institucion=None,
):
    if package.get("format_version") != FORMAT_VERSION:
        raise TenantTransferError("Version de paquete no soportada.")

    records = package.get("records", [])
    if not records:
        raise TenantTransferError("El paquete no contiene registros.")

    id_maps = {}
    source = package.get("source_institucion", {})
    created_institucion = None

    with transaction.atomic(), _mute_predictive_signals():
        if mode == "new":
            inst_record = next((r for r in records if r["model"] == "core.institucion"), None)
            if not inst_record:
                raise TenantTransferError("Falta registro de institucion en el paquete.")
            fields = inst_record["fields"].copy()
            fields["nombre"] = nombre or f"{fields.get('nombre', source.get('nombre', 'Institucion'))} (importada)"
            base_subdominio = subdominio or f"{source.get('subdominio', 'tenant')}-import"
            fields["subdominio"] = _unique_subdominio(base_subdominio)
            fields["activo"] = True
            created_institucion = Institucion.objects.create(**fields)
            id_maps["core.institucion"] = {inst_record["pk"]: created_institucion.pk}
        elif mode == "replace":
            if not target_institucion:
                raise TenantTransferError("Debe indicar la institucion destino para reemplazo.")
            created_institucion = target_institucion
            _clear_tenant_data(target_institucion)
            inst_record = next((r for r in records if r["model"] == "core.institucion"), None)
            if inst_record:
                id_maps["core.institucion"] = {inst_record["pk"]: target_institucion.pk}
        else:
            raise TenantTransferError("Modo de importacion no soportado.")

        import_order = [
            "core.especialidad",
            "auth.user",
            "core.profesional",
            "core.horario",
            "variables_clinicas.variableclinica",
            "pacientes.paciente",
            "portal_paciente.perfilpaciente",
            "citas.cita",
            "preclinica.preclinica",
            "consulta.consulta",
            "consulta.diagnostico",
            "variables_clinicas.valorvariableclinica",
            "referencias.referencia",
            "referencias.contrarreferencia",
            "qr.documentoqr",
            "notificaciones.recordatoriomedicamento",
            "notificaciones.lognotificacion",
            "ia_predictiva.prediccionausentismo",
            "ia_predictiva.demandacita",
            "ia_predictiva.alertariesgocronico",
            "pacientes.documentoocrlog",
        ]

        records_by_model = {}
        for record in records:
            if record["model"] == "core.institucion":
                continue
            records_by_model.setdefault(record["model"], []).append(record)

        for model_label in import_order:
            for record in records_by_model.get(model_label, []):
                if model_label == "auth.user":
                    fields = record["fields"].copy()
                    old_username = fields.get("username", f"user{record['pk']}")
                    fields["username"] = _unique_username(old_username)
                    fields["password"] = make_password(get_random_string(16))
                    fields.pop("groups", None)
                    fields.pop("user_permissions", None)
                    user = User.objects.create(**fields)
                    id_maps.setdefault("auth.user", {})[record["pk"]] = user.pk
                    continue
                _deserialize_record(record, id_maps)

    return created_institucion, id_maps


def _clear_tenant_data(institucion):
    AlertaRiesgoCronico.objects.filter(institucion=institucion).delete()
    PrediccionAusentismo.objects.filter(institucion=institucion).delete()
    DemandaCita.objects.filter(institucion=institucion).delete()
    LogNotificacion.objects.filter(institucion=institucion).delete()
    RecordatorioMedicamento.objects.filter(institucion=institucion).delete()
    DocumentoQR.objects.filter(institucion=institucion).delete()
    Contrarreferencia.objects.filter(institucion=institucion).delete()
    Referencia.objects.filter(institucion=institucion).delete()
    ValorVariableClinica.objects.filter(institucion=institucion).delete()
    Diagnostico.objects.filter(institucion=institucion).delete()
    Consulta.objects.filter(institucion=institucion).delete()
    Preclinica.objects.filter(institucion=institucion).delete()
    Cita.objects.filter(institucion=institucion).delete()
    portal_user_ids = set(
        PerfilPaciente.objects.filter(institucion=institucion).values_list("usuario_id", flat=True)
    )
    PerfilPaciente.objects.filter(institucion=institucion).delete()
    Paciente.objects.filter(institucion=institucion).delete()
    VariableClinica.objects.filter(institucion=institucion).delete()
    Horario.objects.filter(institucion=institucion).delete()
    profesionales = list(Profesional.objects.filter(institucion=institucion))
    user_ids = {p.usuario_id for p in profesionales if p.usuario_id}
    user_ids.update(uid for uid in portal_user_ids if uid)
    Profesional.objects.filter(institucion=institucion).delete()
    Especialidad.objects.filter(institucion=institucion).delete()
    DocumentoOCRLog.objects.filter(institucion=institucion).delete()
    User.objects.filter(pk__in=[uid for uid in user_ids if uid]).delete()


def log_tenant_operation(tipo, institucion, user, archivo="", detalle=""):
    BackupLog.objects.create(
        tipo=tipo,
        alcance="institucion",
        institucion=institucion,
        archivo=archivo,
        usuario=user,
        detalle=detalle,
    )
