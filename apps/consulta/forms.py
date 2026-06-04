from django import forms

from .models import Consulta


class MotivoForm(forms.ModelForm):
    class Meta:
        model = Consulta
        fields = ["motivo_consulta"]


class AnamnesisForm(forms.ModelForm):
    class Meta:
        model = Consulta
        fields = ["anamnesis"]


class ExamenFisicoForm(forms.ModelForm):
    class Meta:
        model = Consulta
        fields = ["examen_fisico"]


class DiagnosticoForm(forms.Form):
    codigo_cie10 = forms.CharField(max_length=10)
    nombre = forms.CharField(max_length=200)
    es_principal = forms.BooleanField(required=False)


class PlanForm(forms.ModelForm):
    class Meta:
        model = Consulta
        fields = ["plan_terapeutico", "conducta"]
