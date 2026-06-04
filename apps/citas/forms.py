from django import forms

from apps.core.models import Especialidad, Profesional
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
        if institucion:
            self.fields["paciente"].queryset = Paciente.objects.filter(institucion=institucion, activo=True)
            self.fields["especialidad"].queryset = Especialidad.objects.filter(institucion=institucion, activo=True)
            self.fields["profesional"].queryset = Profesional.objects.filter(
                institucion=institucion, tipo="medico", activo=True
            )
