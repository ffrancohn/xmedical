from django import forms

from .models import Paciente


class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = [
            "documento",
            "nombre",
            "apellido",
            "fecha_nacimiento",
            "sexo",
            "telefono",
            "telefono_fijo",
            "email",
            "direccion",
            "ciudad",
            "departamento",
            "contacto_emergencia_nombre",
            "contacto_emergencia_telefono",
            "observaciones",
            "activo",
        ]
        widgets = {
            "fecha_nacimiento": forms.DateInput(attrs={"type": "date"}),
            "direccion": forms.Textarea(attrs={"rows": 3}),
            "observaciones": forms.Textarea(attrs={"rows": 3}),
        }
        labels = {
            "telefono": "Telefono movil",
            "telefono_fijo": "Telefono fijo",
            "email": "Correo electronico",
            "contacto_emergencia_nombre": "Contacto de emergencia",
            "contacto_emergencia_telefono": "Telefono de emergencia",
        }
