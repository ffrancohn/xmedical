from django import forms
from django.core.exceptions import ValidationError

from apps.core.models import Especialidad, Horario, Profesional
from apps.pacientes.models import Paciente
from .models import Cita


class CitaForm(forms.ModelForm):
    especialidad = forms.ModelChoiceField(queryset=Especialidad.objects.none(), required=True)

    class Meta:
        model = Cita
        fields = ["paciente", "especialidad", "profesional", "fecha", "hora", "estado"]
        widgets = {"fecha": forms.DateInput(attrs={"type": "date"}), "hora": forms.TimeInput(attrs={"type": "time"})}

    def __init__(self, *args, institucion=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.institucion = institucion
        if institucion:
            self.fields["paciente"].queryset = Paciente.objects.filter(institucion=institucion, activo=True)
            self.fields["especialidad"].queryset = Especialidad.objects.filter(institucion=institucion, activo=True)
            self.fields["profesional"].queryset = Profesional.objects.filter(
                institucion=institucion, tipo="medico", activo=True
            )
        especialidad_id = self.data.get("especialidad") or self.initial.get("especialidad")
        if especialidad_id:
            self.fields["profesional"].queryset = self.fields["profesional"].queryset.filter(
                especialidad_id=especialidad_id
            )

    def clean(self):
        cleaned = super().clean()
        fecha = cleaned.get("fecha")
        hora = cleaned.get("hora")
        profesional = cleaned.get("profesional")
        especialidad = cleaned.get("especialidad")

        if especialidad and profesional and profesional.especialidad_id != especialidad.id:
            raise ValidationError("El medico seleccionado no pertenece a la especialidad indicada.")

        if fecha and hora and profesional:
            horarios = Horario.objects.filter(
                profesional=profesional, dia_semana=fecha.weekday(), activo=True
            )
            if horarios.exists():
                dentro_horario = any(h.hora_inicio <= hora <= h.hora_fin for h in horarios)
                if not dentro_horario:
                    raise ValidationError("La hora seleccionada esta fuera del horario del profesional.")

            conflicto = Cita.objects.filter(
                profesional=profesional, fecha=fecha, hora=hora
            ).exclude(estado="cancelada")
            if self.instance.pk:
                conflicto = conflicto.exclude(pk=self.instance.pk)
            if conflicto.exists():
                raise ValidationError("Ya existe una cita activa en ese horario para el profesional.")

        return cleaned


class CitaFlexibleForm(forms.Form):
    JORNADA_CHOICES = [
        ("manana", "Manana"),
        ("tarde", "Tarde"),
        ("cualquiera", "Cualquiera"),
    ]

    paciente = forms.ModelChoiceField(queryset=Paciente.objects.none())
    especialidad = forms.ModelChoiceField(queryset=Especialidad.objects.none())
    profesional = forms.ModelChoiceField(
        queryset=Profesional.objects.none(), required=False, label="Medico (opcional)"
    )
    fecha_inicio = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
    fecha_fin = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
    jornada = forms.ChoiceField(choices=JORNADA_CHOICES, initial="cualquiera")

    def __init__(self, *args, institucion=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.institucion = institucion
        if institucion:
            self.fields["paciente"].queryset = Paciente.objects.filter(institucion=institucion, activo=True)
            self.fields["especialidad"].queryset = Especialidad.objects.filter(institucion=institucion, activo=True)
            self.fields["profesional"].queryset = Profesional.objects.filter(
                institucion=institucion, tipo="medico", activo=True
            )
        especialidad_id = self.data.get("especialidad") or self.initial.get("especialidad")
        if especialidad_id:
            self.fields["profesional"].queryset = self.fields["profesional"].queryset.filter(
                especialidad_id=especialidad_id
            )

    def clean(self):
        cleaned = super().clean()
        fecha_inicio = cleaned.get("fecha_inicio")
        fecha_fin = cleaned.get("fecha_fin")
        if fecha_inicio and fecha_fin and fecha_fin < fecha_inicio:
            raise ValidationError("La fecha fin no puede ser anterior a la fecha inicio.")
        profesional = cleaned.get("profesional")
        especialidad = cleaned.get("especialidad")
        if profesional and especialidad and profesional.especialidad_id != especialidad.id:
            raise ValidationError("El medico seleccionado no pertenece a la especialidad indicada.")
        return cleaned
