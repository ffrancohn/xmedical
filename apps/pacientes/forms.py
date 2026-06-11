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


class PacientePublicForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = [
            "documento",
            "nombre",
            "apellido",
            "fecha_nacimiento",
            "sexo",
            "telefono",
            "email",
            "direccion",
            "ciudad",
            "departamento",
        ]
        widgets = {
            "fecha_nacimiento": forms.DateInput(attrs={"type": "date", "class": "input input-bordered w-full"}),
            "documento": forms.TextInput(attrs={"class": "input input-bordered w-full"}),
            "nombre": forms.TextInput(attrs={"class": "input input-bordered w-full"}),
            "apellido": forms.TextInput(attrs={"class": "input input-bordered w-full"}),
            "sexo": forms.Select(attrs={"class": "select select-bordered w-full"}),
            "telefono": forms.TextInput(attrs={"class": "input input-bordered w-full"}),
            "email": forms.EmailInput(attrs={"class": "input input-bordered w-full"}),
            "direccion": forms.Textarea(attrs={"rows": 2, "class": "textarea textarea-bordered w-full"}),
            "ciudad": forms.TextInput(attrs={"class": "input input-bordered w-full"}),
            "departamento": forms.TextInput(attrs={"class": "input input-bordered w-full"}),
        }
        labels = {
            "telefono": "Telefono movil",
            "email": "Correo electronico",
        }
