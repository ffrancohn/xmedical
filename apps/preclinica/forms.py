from decimal import Decimal

from django import forms

from .models import Preclinica


class PreclinicaForm(forms.ModelForm):
    class Meta:
        model = Preclinica
        exclude = ["institucion", "cita", "imc", "creado_en"]

    def save(self, commit=True):
        preclinica = super().save(commit=False)
        peso = self.cleaned_data.get("peso")
        talla = self.cleaned_data.get("talla")
        if peso and talla:
            preclinica.imc = (peso / (talla * talla)).quantize(Decimal("0.01"))
        if commit:
            preclinica.save()
        return preclinica
