from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from apps.core.models import Especialidad, Institucion, Profesional
from .models import UserPreference


class XMedicalAuthenticationForm(AuthenticationForm):
    institucion = forms.ModelChoiceField(
        queryset=Institucion.objects.filter(activo=True).order_by("nombre"),
        required=False,
        label="Institución",
        empty_label="Selecciona tu clínica",
    )

    def __init__(self, *args, show_institucion=False, patient_mode=False, **kwargs):
        super().__init__(*args, **kwargs)
        self.show_institucion = show_institucion
        self.patient_mode = patient_mode
        if not show_institucion:
            self.fields.pop("institucion", None)
        self.fields["username"].label = "Correo electrónico" if patient_mode else "Usuario"
        if patient_mode:
            self.fields["username"].widget.attrs.setdefault(
                "placeholder",
                "tu.correo@ejemplo.com",
            )

    def clean(self):
        username = (self.cleaned_data.get("username") or self.data.get("username") or "").strip()
        if "@" in username:
            self.cleaned_data["username"] = username.lower()
        return super().clean()


class ProfesionalRegistroForm(UserCreationForm):
    institucion = forms.ModelChoiceField(queryset=Institucion.objects.filter(activo=True))
    especialidad = forms.ModelChoiceField(queryset=Especialidad.objects.filter(activo=True), required=False)
    nombre = forms.CharField(max_length=100)
    tipo = forms.ChoiceField(choices=Profesional.TIPO_CHOICES)
    registro_medico = forms.CharField(max_length=50, required=False)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1", "password2")

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("tipo") == "medico" and not cleaned.get("especialidad"):
            self.add_error("especialidad", "La especialidad es obligatoria para medicos.")
        return cleaned

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
