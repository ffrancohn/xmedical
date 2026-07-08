from django import forms

from .models import ValorVariableClinica, VariableClinica


def _campo_para_variable(variable: VariableClinica):
    field_name = f"var_{variable.pk}"
    widget_attrs = {"class": "input input-bordered w-full"}
    if variable.tipo == "texto":
        return field_name, forms.CharField(
            label=variable.nombre,
            required=variable.obligatorio,
            widget=forms.Textarea(attrs={**widget_attrs, "rows": 3}),
        )
    if variable.tipo == "numero":
        return field_name, forms.DecimalField(label=variable.nombre, required=variable.obligatorio, widget=forms.NumberInput(attrs=widget_attrs))
    if variable.tipo == "booleano":
        return field_name, forms.BooleanField(label=variable.nombre, required=variable.obligatorio)
    if variable.tipo == "fecha":
        return field_name, forms.DateField(
            label=variable.nombre,
            required=variable.obligatorio,
            widget=forms.DateInput(attrs={**widget_attrs, "type": "date"}),
        )
    if variable.tipo == "select":
        opciones = [(opcion, opcion) for opcion in variable.opciones if opcion]
        return field_name, forms.ChoiceField(
            label=variable.nombre,
            choices=opciones,
            required=variable.obligatorio,
            widget=forms.Select(attrs=widget_attrs),
        )
    return field_name, forms.CharField(label=variable.nombre, required=variable.obligatorio, widget=forms.TextInput(attrs=widget_attrs))


def build_variables_form(variables, consulta, data=None):
    fields = {}
    initial = {}
    valores = {
        valor.variable_id: valor
        for valor in ValorVariableClinica.objects.filter(consulta=consulta, variable__in=variables)
    }
    for variable in variables:
        field_name, field = _campo_para_variable(variable)
        fields[field_name] = field
        valor = valores.get(variable.pk)
        if valor:
            if variable.tipo == "booleano":
                initial[field_name] = valor.valor in ("1", "true", "True", "on")
            elif variable.tipo == "numero" and valor.valor:
                initial[field_name] = valor.valor
            else:
                initial[field_name] = valor.valor

    form_class = type("VariablesClinicasForm", (forms.Form,), fields)
    return form_class(data, initial=initial) if data is not None else form_class(initial=initial)


def guardar_valores_variables(consulta, variables, cleaned_data):
    for variable in variables:
        field_name = f"var_{variable.pk}"
        if field_name not in cleaned_data:
            continue
        valor = cleaned_data[field_name]
        if variable.tipo == "booleano":
            texto = "1" if valor else "0"
        elif valor is None:
            texto = ""
        else:
            texto = str(valor)
        ValorVariableClinica.objects.update_or_create(
            consulta=consulta,
            variable=variable,
            defaults={"institucion": consulta.institucion, "valor": texto},
        )
