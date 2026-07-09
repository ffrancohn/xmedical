import json
from io import BytesIO

from django.utils import timezone

from apps.consulta.models import Consulta


def consultas_para_paciente(paciente, institucion):
    consultas = (
        Consulta.objects.select_related("cita", "cita__profesional", "cita__profesional__especialidad")
        .prefetch_related("diagnosticos", "valores_variables__variable")
        .filter(cita__paciente=paciente)
        .order_by("-creado_en")
    )
    if institucion:
        consultas = consultas.filter(institucion=institucion)
    return consultas


def serializar_hce(paciente, institucion):
    consultas = consultas_para_paciente(paciente, institucion)
    return {
        "paciente": {
            "documento": paciente.documento,
            "nombre": paciente.nombre,
            "apellido": paciente.apellido,
            "fecha_nacimiento": paciente.fecha_nacimiento.isoformat()
            if paciente.fecha_nacimiento
            else None,
            "sexo": paciente.sexo,
            "institucion": institucion.nombre if institucion else None,
        },
        "exportado_en": timezone.now().isoformat(),
        "consultas": [
            {
                "fecha": consulta.creado_en.isoformat(),
                "motivo_consulta": consulta.motivo_consulta,
                "anamnesis": consulta.anamnesis,
                "examen_fisico": consulta.examen_fisico,
                "plan_terapeutico": consulta.plan_terapeutico,
                "conducta": consulta.conducta,
                "profesional": consulta.cita.profesional.nombre,
                "especialidad": (
                    consulta.cita.profesional.especialidad.nombre
                    if consulta.cita.profesional.especialidad_id
                    else None
                ),
                "diagnosticos": [
                    {
                        "codigo_cie10": dx.codigo_cie10,
                        "nombre": dx.nombre,
                        "es_principal": dx.es_principal,
                    }
                    for dx in consulta.diagnosticos.all()
                ],
                "variables_clinicas": [
                    {
                        "nombre": valor.variable.nombre,
                        "valor": valor.valor_mostrar,
                    }
                    for valor in consulta.valores_variables.all()
                ],
            }
            for consulta in consultas
        ],
    }


def exportar_hce_json(paciente, institucion):
    data = serializar_hce(paciente, institucion)
    return json.dumps(data, ensure_ascii=False, indent=2)


def exportar_hce_pdf(paciente, institucion):
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas

    data = serializar_hce(paciente, institucion)
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    y = height - 50

    def write_line(text, indent=50, size=10):
        nonlocal y
        if y < 60:
            pdf.showPage()
            y = height - 50
        pdf.setFont("Helvetica", size)
        pdf.drawString(indent, y, text[:110])
        y -= size + 4

    write_line("XMedical - Historia clinica portatil", indent=50, size=14)
    write_line(f"Paciente: {data['paciente']['nombre']} {data['paciente']['apellido']}")
    write_line(f"Documento: {data['paciente']['documento']}")
    if data["paciente"]["institucion"]:
        write_line(f"Institucion: {data['paciente']['institucion']}")
    write_line(f"Exportado: {data['exportado_en'][:19]}")
    y -= 8

    for consulta in data["consultas"]:
        write_line(f"Consulta {consulta['fecha'][:10]}", size=12)
        write_line(f"Profesional: {consulta['profesional']}")
        if consulta["especialidad"]:
            write_line(f"Especialidad: {consulta['especialidad']}")
        if consulta["motivo_consulta"]:
            write_line(f"Motivo: {consulta['motivo_consulta']}")
        if consulta["plan_terapeutico"]:
            write_line(f"Plan: {consulta['plan_terapeutico']}")
        for dx in consulta["diagnosticos"]:
            principal = " (principal)" if dx["es_principal"] else ""
            write_line(f"Dx: {dx['codigo_cie10']} - {dx['nombre']}{principal}")
        y -= 6

    if not data["consultas"]:
        write_line("Sin consultas registradas.")

    pdf.save()
    buffer.seek(0)
    return buffer.getvalue()
