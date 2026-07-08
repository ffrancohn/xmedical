import calendar
from datetime import datetime, timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import QueryDict
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views import View
from django.views.generic import ListView

from apps.core.permissions import (
    CAN_AGENDAR_CITAS,
    CAN_CANCELAR_CITAS,
    CAN_LIST_CITAS,
    RecepcionRequiredMixin,
    RoleRequiredMixin,
    role_required,
)
from apps.core.views import current_institucion, institution_filter_context, selected_instituciones
from .forms import CitaFlexibleForm, CitaForm
from .models import Cita
from .services import FlexibleAgendamientoService, SinTurnosDisponiblesError


class CitaListView(LoginRequiredMixin, RoleRequiredMixin, ListView):
    allowed_roles = CAN_LIST_CITAS
    model = Cita
    template_name = "citas/lista.html"
    context_object_name = "citas"

    def get_queryset(self):
        qs = Cita.objects.select_related(
            "paciente", "profesional", "prediccion_ausentismo"
        ).all()
        instituciones, _ = selected_instituciones(self.request)
        qs = qs.filter(institucion__in=instituciones)
        return qs.order_by("fecha", "hora")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        selected_date = parse_date_or_today(self.request.GET.get("fecha"))
        vista = self.request.GET.get("vista", "lista")
        citas = list(self.get_queryset())
        context.update(
            {
                "vista": vista,
                "selected_date": selected_date,
                "prev_date": navigation_date(selected_date, vista, -1),
                "next_date": navigation_date(selected_date, vista, 1),
                "today": timezone.localdate(),
                "citas_dia": [c for c in citas if c.fecha == selected_date],
                "semana": build_week(selected_date, citas),
                "mes": build_month(selected_date, citas),
                "dos_meses": [build_month(selected_date, citas), build_month(add_months(selected_date, 1), citas)],
                "tres_meses": [
                    build_month(selected_date, citas),
                    build_month(add_months(selected_date, 1), citas),
                    build_month(add_months(selected_date, 2), citas),
                ],
            }
        )
        context.update(institution_filter_context(self.request))
        context["institution_query"] = institutions_query_string(self.request)
        return context


class CitaCreateView(LoginRequiredMixin, RecepcionRequiredMixin, View):
    template_name = "citas/form.html"

    def get(self, request):
        return render(request, self.template_name, {"form": CitaForm(institucion=current_institucion(request))})

    def post(self, request):
        institucion = current_institucion(request)
        form = CitaForm(request.POST, institucion=institucion)
        if form.is_valid():
            cita = form.save(commit=False)
            cita.institucion = institucion
            cita.tipo_agendamiento = "especifico"
            cita.save()
            messages.success(request, "Cita agendada correctamente.")
            return redirect("citas_lista")
        return render(request, self.template_name, {"form": form})


class CitaFlexibleCreateView(LoginRequiredMixin, RecepcionRequiredMixin, View):
    template_name = "citas/form_flexible.html"
    resultado_template = "citas/flexible_resultado.html"

    def get(self, request):
        institucion = current_institucion(request)
        return render(request, self.template_name, {"form": CitaFlexibleForm(institucion=institucion)})

    def post(self, request):
        institucion = current_institucion(request)
        if not institucion:
            messages.error(request, "No se pudo identificar la institucion.")
            return redirect("citas_lista")
        form = CitaFlexibleForm(request.POST, institucion=institucion)
        if not form.is_valid():
            return render(request, self.template_name, {"form": form})

        service = FlexibleAgendamientoService(institucion)
        try:
            cita = service.asignar_primer_turno(
                paciente=form.cleaned_data["paciente"],
                especialidad=form.cleaned_data["especialidad"],
                fecha_inicio=form.cleaned_data["fecha_inicio"],
                fecha_fin=form.cleaned_data["fecha_fin"],
                jornada=form.cleaned_data["jornada"],
                profesional=form.cleaned_data.get("profesional"),
            )
        except SinTurnosDisponiblesError as exc:
            messages.error(request, str(exc))
            return render(request, self.template_name, {"form": form, "sin_turnos": True})

        messages.success(request, "Cita flexible asignada automaticamente.")
        return render(request, self.resultado_template, {"cita": cita, "form": form})


@login_required
@role_required(*CAN_CANCELAR_CITAS)
def cancelar_cita(request, pk):
    qs = Cita.objects.all()
    institucion = current_institucion(request)
    if institucion:
        qs = qs.filter(institucion=institucion)
    cita = get_object_or_404(qs, pk=pk)
    cita_datetime = timezone.make_aware(datetime.combine(cita.fecha, cita.hora))
    if cita_datetime - timezone.now() < timedelta(hours=2):
        messages.error(request, "Las citas solo pueden cancelarse con al menos 2 horas de anticipacion.")
        return redirect("citas_lista")
    cita.estado = "cancelada"
    cita.save(update_fields=["estado"])
    messages.info(request, "Cita cancelada.")
    return redirect("citas_lista")


def institutions_query_string(request):
    values = request.GET.getlist("instituciones")
    if not values:
        return ""
    query = QueryDict(mutable=True)
    for value in values:
        query.appendlist("instituciones", value)
    return "&" + query.urlencode()


def parse_date_or_today(value):
    if not value:
        return timezone.localdate()
    try:
        return timezone.datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        return timezone.localdate()


def navigation_date(date, vista, direction):
    if vista == "semana":
        return date + timedelta(days=7 * direction)
    if vista == "mes":
        return add_months(date, direction)
    if vista == "dos_meses":
        return add_months(date, 2 * direction)
    if vista == "tres_meses":
        return add_months(date, 3 * direction)
    return date + timedelta(days=direction)


def add_months(date, months):
    month = date.month - 1 + months
    year = date.year + month // 12
    month = month % 12 + 1
    day = min(date.day, calendar.monthrange(year, month)[1])
    return date.replace(year=year, month=month, day=day)


def citas_by_date(citas):
    grouped = {}
    for cita in citas:
        grouped.setdefault(cita.fecha, []).append(cita)
    return grouped


def build_week(date, citas):
    grouped = citas_by_date(citas)
    start = date - timedelta(days=date.weekday())
    return [{"date": start + timedelta(days=i), "citas": grouped.get(start + timedelta(days=i), [])} for i in range(7)]


def build_month(date, citas):
    grouped = citas_by_date(citas)
    cal = calendar.Calendar(firstweekday=0)
    weeks = []
    for week in cal.monthdatescalendar(date.year, date.month):
        weeks.append(
            [
                {
                    "date": day,
                    "in_month": day.month == date.month,
                    "citas": grouped.get(day, []),
                }
                for day in week
            ]
        )
    return {"date": date, "label": date.strftime("%B %Y").capitalize(), "weeks": weeks}
