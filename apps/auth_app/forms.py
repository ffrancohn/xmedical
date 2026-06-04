from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from apps.core.models import Especialidad, Institucion, Profesional
from .models import UserPreference


class ProfesionalRegistroForm(UserCreationForm):
    institucion = forms.ModelChoiceField(queryset=Institucion.objects.filter(activo=True))
    especialidad = forms.ModelChoiceField(queryset=Especialidad.objects.filter(activo=True), required=False)
    nombre = forms.CharField(max_length=100)
    tipo = forms.ChoiceField(choices=Profesional.TIPO_CHOICES)
    registro_medico = forms.CharField(max_length=50, required=False)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            Profesional.objects.create(
                usuario=user,
                institucion=self.cleaned_data["institucion"],
                especialidad=self.cleaned_data.get("especialidad"),
                nombre=self.cleaned_data["nombre"],
                tipo=self.cleaned_data["tipo"],
                registro_medico=self.cleaned_data.get("registro_medico", ""),
            )
        return user


class UserPreferenceForm(forms.ModelForm):
    class Meta:
        model = UserPreference
        fields = ["theme"]
        labels = {"theme": "Tema visual"}
