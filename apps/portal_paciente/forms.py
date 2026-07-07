from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

from apps.core.models import Especialidad, Profesional
from apps.pacientes.models import Paciente

from .models import PerfilPaciente


class PortalRegistroForm(forms.Form):
    documento = forms.CharField(max_length=20, label="Documento de identidad")
    nombre = forms.CharField(max_length=100)
    apellido = forms.CharField(max_length=100)
    email = forms.EmailField()
    telefono = forms.CharField(max_length=20, required=False)
    fecha_nacimiento = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}),
    )
    password1 = forms.CharField(widget=forms.PasswordInput, label="Contrasena")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirmar contrasena")

    def __init__(self, *args, institucion=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.institucion = institucion

    def clean_documento(self):
        documento = self.cleaned_data["documento"].strip()
        if not documento:
            raise forms.ValidationError("El documento es obligatorio.")
        return documento

    def clean(self):
        cleaned = super().clean()
        password1 = cleaned.get("password1")
        password2 = cleaned.get("password2")
        if password1 and password2 and password1 != password2:
            self.add_error("password2", "Las contrasenas no coinciden.")
        if password1:
            validate_password(password1)
        if not self.institucion:
            raise forms.ValidationError("No se pudo identificar la institucion.")
        documento = cleaned.get("documento")
        if documento:
            paciente = Paciente.objects.filter(
                institucion=self.institucion, documento=documento
            ).first()
            if paciente and hasattr(paciente, "perfil_portal"):
                self.add_error(
                    "documento",
                    "Este paciente ya tiene una cuenta en el portal.",
                )
        email = cleaned.get("email")
        if email and User.objects.filter(username=email).exists():
            self.add_error("email", "Ya existe una cuenta con este correo.")
        return cleaned

    def save(self):
        documento = self.cleaned_data["documento"]
        paciente = Paciente.objects.filter(
            institucion=self.institucion, documento=documento
        ).first()
        if not paciente:
            paciente = Paciente.objects.create(
                institucion=self.institucion,
                documento=documento,
                nombre=self.cleaned_data["nombre"],
                apellido=self.cleaned_data["apellido"],
                email=self.cleaned_data["email"],
                telefono=self.cleaned_data.get("telefono", ""),
                fecha_nacimiento=self.cleaned_data.get("fecha_nacimiento"),
                activo=True,
            )
        else:
            paciente.email = self.cleaned_data["email"]
            if self.cleaned_data.get("telefono"):
                paciente.telefono = self.cleaned_data["telefono"]
            paciente.save()

        user = User.objects.create_user(
            username=self.cleaned_data["email"],
            email=self.cleaned_data["email"],
            password=self.cleaned_data["password1"],
            first_name=self.cleaned_data["nombre"],
            last_name=self.cleaned_data["apellido"],
        )
        return PerfilPaciente.objects.create(
            institucion=self.institucion,
            usuario=user,
            paciente=paciente,
        )


class PortalCitaFlexibleForm(forms.Form):
    JORNADA_CHOICES = [
        ("manana", "Manana"),
        ("tarde", "Tarde"),
        ("cualquiera", "Cualquiera"),
    ]

    especialidad = forms.ModelChoiceField(queryset=Especialidad.objects.none())
    profesional = forms.ModelChoiceField(
        queryset=Profesional.objects.none(),
        required=False,
        label="Medico (opcional)",
    )
    fecha_inicio = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
    fecha_fin = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
    jornada = forms.ChoiceField(choices=JORNADA_CHOICES, initial="cualquiera")

    def __init__(self, *args, institucion=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.institucion = institucion
        if institucion:
            self.fields["especialidad"].queryset = Especialidad.objects.filter(
                institucion=institucion, activo=True
            )
            self.fields["profesional"].queryset = Profesional.objects.filter(
                institucion=institucion, tipo="medico", activo=True
            )
