from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from apps.citas.models import Cita
from apps.core.views import current_institucion
from apps.pacientes.models import Paciente
from .forms import AnamnesisForm, DiagnosticoForm, ExamenFisicoForm, MotivoForm, PlanForm
from .models import Consulta, Diagnostico
from .wizard import CIE10_MVP, STEPS


class ConsultaWizardView(LoginRequiredMixin, View):
    template_name = "consulta/wizard.html"

    def get_consulta(self, request, cita):
        consulta, _ = Consulta.objects.get_or_create(institucion=current_institucion(request), cita=cita)
        return consulta

    def get(self, request, cita_id, step=1):
        step = int(step)
        cita = get_object_or_404(
            Cita.objects.select_related("paciente", "profesional"),
            pk=cita_id,
            institucion=current_institucion(request),
        )
        consulta = self.get_consulta(request, cita)
        context = self.context_for_step(step, cita, consulta)
        return render(request, self.template_name, context)

    def post(self, request, cita_id, step=1):
        step = int(step)
        institucion = current_institucion(request)
        cita = get_object_or_404(Cita, pk=cita_id, institucion=institucion)
        consulta = self.get_consulta(request, cita)

        if step in [1, 7]:
            if step == 7:
                cita.estado = "atendida"
                cita.save(update_fields=["estado"])
                messages.success(request, "Consulta finalizada.")
                return redirect("dashboard")
            return redirect("consulta_wizard", cita_id=cita.id, step=2)

        form = self.form_for_step(step, request.POST, consulta)
        if form and form.is_valid():
            if step == 5:
                Diagnostico.objects.create(
                    institucion=institucion,
                    consulta=consulta,
                    codigo_cie10=form.cleaned_data["codigo_cie10"],
                    nombre=form.cleaned_data["nombre"],
                    es_principal=form.cleaned_data["es_principal"],
                    orden=consulta.diagnosticos.count() + 1,
                )
            else:
                form.save()
            return redirect("consulta_wizard", cita_id=cita.id, step=min(step + 1, 7))

        context = self.context_for_step(step, cita, consulta)
        context["form"] = form
        return render(request, self.template_name, context)

    def form_for_step(self, step, data=None, consulta=None):
        forms = {2: MotivoForm, 3: AnamnesisForm, 4: ExamenFisicoForm, 5: DiagnosticoForm, 6: PlanForm}
        form_class = forms.get(step)
        if not form_class:
            return None
        if step == 5:
            return form_class(data)
        return form_class(data, instance=consulta)

    def context_for_step(self, step, cita, consulta):
        return {
            "step": step,
            "steps": STEPS,
            "step_name": STEPS[step],
            "cita": cita,
            "consulta": consulta,
            "preclinica": getattr(cita, "preclinica", None),
            "form": self.form_for_step(step, consulta=consulta),
            "cie10": CIE10_MVP,
        }


def cie10_search(request):
    q = request.GET.get("q", "").lower()
    results = [item for item in CIE10_MVP if q in item["codigo"].lower() or q in item["nombre"].lower()] if q else CIE10_MVP
    return JsonResponse({"results": results[:10]})


def historia_clinica(request, paciente_id):
    institucion = current_institucion(request)
    paciente_qs = Paciente.objects.all()
    if institucion:
        paciente_qs = paciente_qs.filter(institucion=institucion)
    paciente = get_object_or_404(paciente_qs, pk=paciente_id)
    consultas = Consulta.objects.select_related("cita").prefetch_related("diagnosticos").filter(cita__paciente=paciente)
    if institucion:
        consultas = consultas.filter(institucion=institucion)
    return render(request, "consulta/historia.html", {"paciente": paciente, "consultas": consultas})
