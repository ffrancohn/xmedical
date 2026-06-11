from django import forms

from apps.citas.models import Cita
from apps.core.models import Especialidad
from .models import Contrarreferencia, Referencia


class ReferenciaForm(forms.ModelForm):
    class Meta:
        model = Referencia
        fields = ["especialidad_destino", "prioridad", "motivo"]
        widgets = {
            "motivo": forms.Textarea(attrs={"rows": 4, "class": "textarea textarea-bordered w-full"}),
            "prioridad": forms.Select(attrs={"class": "select select-bordered w-full"}),
            "especialidad_destino": forms.Select(attrs={"class": "select select-bordered w-full"}),
        }

    def __init__(self, *args, institucion=None, **kwargs):
        super().__init__(*args, **kwargs)
        if institucion:
            self.fields["especialidad_destino"].queryset = Especialidad.objects.filter(
                institucion=institucion, nivel="segundo", activo=True
            )


class ReferenciaRespuestaForm(forms.Form):
    comentarios_especialista = forms.CharField(
        label="Comentarios",
        widget=forms.Textarea(attrs={"rows": 3, "class": "textarea textarea-bordered w-full"}),
        required=False,
    )


class ReferenciaAgendarForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = ["fecha", "hora"]
        widgets = {
            "fecha": forms.DateInput(attrs={"type": "date", "class": "input input-bordered w-full"}),
            "hora": forms.TimeInput(attrs={"type": "time", "class": "input input-bordered w-full"}),
        }

    def __init__(self, *args, referencia=None, institucion=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.referencia = referencia
        self.institucion = institucion

    def clean(self):
        cleaned = super().clean()
        if not self.referencia or not self.institucion:
            return cleaned
        fecha = cleaned.get("fecha")
        hora = cleaned.get("hora")
        profesional = self.referencia.especialista
        if fecha and hora and profesional:
            from apps.citas.models import Cita
            from apps.core.models import Horario

            horarios = Horario.objects.filter(
                profesional=profesional, dia_semana=fecha.weekday(), activo=True
            )
            if horarios.exists():
                dentro_horario = any(h.hora_inicio <= hora <= h.hora_fin for h in horarios)
                if not dentro_horario:
                    raise forms.ValidationError("La hora seleccionada esta fuera del horario del especialista.")
            conflicto = Cita.objects.filter(profesional=profesional, fecha=fecha, hora=hora).exclude(
                estado="cancelada"
            )
            if conflicto.exists():
                raise forms.ValidationError("Ya existe una cita activa en ese horario.")
        return cleaned


class ContrarreferenciaForm(forms.ModelForm):
    class Meta:
        model = Contrarreferencia
        fields = ["resumen_atencion", "plan_seguimiento"]
        widgets = {
            "resumen_atencion": forms.Textarea(attrs={"rows": 4, "class": "textarea textarea-bordered w-full"}),
            "plan_seguimiento": forms.Textarea(attrs={"rows": 4, "class": "textarea textarea-bordered w-full"}),
        }
