from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from apps.citas.models import Cita
from apps.core.views import current_institucion
from apps.pacientes.models import Paciente
from apps.variables_clinicas.forms import build_variables_form, guardar_valores_variables
from apps.variables_clinicas.services import variables_para_cita
from .forms import AnamnesisForm, DiagnosticoForm, ExamenFisicoForm, MotivoForm, PlanForm
from .models import Consulta, Diagnostico
from .wizard import CIE10_MVP, FINAL_STEP, STEPS, VARIABLES_STEP, paso_anterior, siguiente_paso


class ConsultaWizardView(LoginRequiredMixin, View):
    template_name = "consulta/wizard.html"

    def get_consulta(self, request, cita):
        consulta, _ = Consulta.objects.get_or_create(institucion=current_institucion(request), cita=cita)
        return consulta

    def get_cita(self, request, cita_id):
        return get_object_or_404(
            Cita.objects.select_related("paciente", "profesional", "profesional__especialidad"),
            pk=cita_id,
            institucion=current_institucion(request),
        )

    def get(self, request, cita_id, step=1):
        step = int(step)
        cita = self.get_cita(request, cita_id)
        if step == VARIABLES_STEP and not variables_para_cita(cita).exists():
            return redirect("consulta_wizard", cita_id=cita.id, step=siguiente_paso(step, cita))
        consulta = self.get_consulta(request, cita)
        context = self.context_for_step(step, cita, consulta)
        return render(request, self.template_name, context)

    def post(self, request, cita_id, step=1):
        step = int(step)
        institucion = current_institucion(request)
        cita = get_object_or_404(
            Cita.objects.select_related("profesional", "profesional__especialidad"),
            pk=cita_id,
            institucion=institucion,
        )
        consulta = self.get_consulta(request, cita)

        if step in [1, FINAL_STEP]:
            if step == FINAL_STEP:
                cita.estado = "atendida"
                cita.save(update_fields=["estado"])
                messages.success(request, "Consulta finalizada.")
                return redirect("dashboard")
            return redirect("consulta_wizard", cita_id=cita.id, step=siguiente_paso(step, cita))

        if step == VARIABLES_STEP:
            variables = list(variables_para_cita(cita))
            form = build_variables_form(variables, consulta, request.POST)
            if form.is_valid():
                guardar_valores_variables(consulta, variables, form.cleaned_data)
                return redirect("consulta_wizard", cita_id=cita.id, step=siguiente_paso(step, cita))
            context = self.context_for_step(step, cita, consulta)
            context["form"] = form
            context["variables"] = variables
            return render(request, self.template_name, context)

        form = self.form_for_step(step, request.POST, consulta)
        if form and form.is_valid():
            if step == 6:
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
            return redirect("consulta_wizard", cita_id=cita.id, step=siguiente_paso(step, cita))

        context = self.context_for_step(step, cita, consulta)
        context["form"] = form
        return render(request, self.template_name, context)

    def form_for_step(self, step, data=None, consulta=None):
        forms = {2: MotivoForm, 3: AnamnesisForm, 4: ExamenFisicoForm, 6: DiagnosticoForm, 7: PlanForm}
        form_class = forms.get(step)
        if not form_class:
            return None
        if step == 6:
            return form_class(data)
        return form_class(data, instance=consulta)

    def context_for_step(self, step, cita, consulta):
        variables = list(variables_para_cita(cita))
        context = {
            "step": step,
            "steps": STEPS,
            "step_name": STEPS[step],
            "cita": cita,
            "consulta": consulta,
            "preclinica": getattr(cita, "preclinica", None),
            "cie10": CIE10_MVP,
            "variables": variables,
            "paso_anterior": paso_anterior(step, cita),
        }
        if step == VARIABLES_STEP:
            context["form"] = build_variables_form(variables, consulta)
        else:
            context["form"] = self.form_for_step(step, consulta=consulta)
        return context


@login_required
def cie10_search(request):
    q = request.GET.get("q", "").lower()
    results = [item for item in CIE10_MVP if q in item["codigo"].lower() or q in item["nombre"].lower()] if q else CIE10_MVP
    return JsonResponse({"results": results[:10]})


@login_required
def historia_clinica(request, paciente_id):
    institucion = current_institucion(request)
    paciente_qs = Paciente.objects.all()
    if institucion:
        paciente_qs = paciente_qs.filter(institucion=institucion)
    paciente = get_object_or_404(paciente_qs, pk=paciente_id)
    consultas = (
        Consulta.objects.select_related("cita")
        .prefetch_related("diagnosticos", "valores_variables__variable")
        .filter(cita__paciente=paciente)
    )
    if institucion:
        consultas = consultas.filter(institucion=institucion)
    return render(request, "consulta/historia.html", {"paciente": paciente, "consultas": consultas})
