from django import forms

from apps.core.ai_institution_config import AI_PROVIDER_CHOICES, default_ai_settings


class ConfiguracionIAForm(forms.Form):
    provider = forms.ChoiceField(
        label="Proveedor",
        choices=AI_PROVIDER_CHOICES,
        widget=forms.RadioSelect,
    )
    ollama_base_url = forms.CharField(
        label="URL Ollama",
        required=False,
        widget=forms.URLInput(attrs={"class": "input input-bordered w-full", "placeholder": "http://localhost:11434"}),
    )
    model = forms.CharField(
        label="Modelo de texto",
        max_length=120,
        widget=forms.TextInput(attrs={"class": "input input-bordered w-full", "list": "ollama-modelos"}),
    )
    vision_model = forms.CharField(
        label="Modelo de visión",
        max_length=120,
        required=False,
        widget=forms.TextInput(attrs={"class": "input input-bordered w-full", "list": "ollama-modelos"}),
    )
    temperature = forms.FloatField(
        label="Temperatura",
        min_value=0.0,
        max_value=1.0,
        widget=forms.NumberInput(attrs={"class": "range range-primary", "step": "0.1", "min": "0", "max": "1"}),
    )
    enabled = forms.BooleanField(
        label="IA habilitada para esta institución",
        required=False,
        initial=True,
    )
    fallback_cloud = forms.BooleanField(
        label="Fallback a cloud si Ollama falla",
        required=False,
    )
    feature_diagnostico_sugerido = forms.BooleanField(
        label="Sugerencia diagnóstica (wizard paso 5)",
        required=False,
        initial=True,
    )
    feature_resumen_clinico = forms.BooleanField(
        label="Resumen clínico",
        required=False,
        initial=True,
    )
    feature_ocr_asistido = forms.BooleanField(
        label="OCR asistido (documentos paciente)",
        required=False,
        initial=True,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        defaults = default_ai_settings()
        if not self.is_bound:
            self.fields["provider"].initial = defaults["provider"]
            self.fields["ollama_base_url"].initial = defaults["ollama_base_url"]
            self.fields["model"].initial = defaults["model"]
            self.fields["vision_model"].initial = defaults["vision_model"]
            self.fields["temperature"].initial = defaults["temperature"]
            self.fields["enabled"].initial = defaults["enabled"]
            self.fields["fallback_cloud"].initial = defaults["fallback_cloud"]
            features = defaults["features"]
            self.fields["feature_diagnostico_sugerido"].initial = features["diagnostico_sugerido"]
            self.fields["feature_resumen_clinico"].initial = features["resumen_clinico"]
            self.fields["feature_ocr_asistido"].initial = features["ocr_asistido"]

    def clean(self):
        cleaned = super().clean()
        provider = cleaned.get("provider")
        if provider == "ollama" and not cleaned.get("ollama_base_url"):
            self.add_error("ollama_base_url", "Indica la URL del servidor Ollama.")
        if provider == "ollama" and not cleaned.get("model"):
            self.add_error("model", "Indica el modelo de texto para Ollama.")
        return cleaned

    def clean_ollama_base_url(self):
        value = (self.cleaned_data.get("ollama_base_url") or "").strip()
        if not value:
            return value
        if not value.startswith(("http://", "https://")):
            value = f"http://{value}"
        return value.rstrip("/")

    @classmethod
    def from_institution_settings(cls, settings_dict):
        features = settings_dict.get("features") or {}
        return cls(
            initial={
                "provider": settings_dict.get("provider"),
                "ollama_base_url": settings_dict.get("ollama_base_url"),
                "model": settings_dict.get("model"),
                "vision_model": settings_dict.get("vision_model"),
                "temperature": settings_dict.get("temperature"),
                "enabled": settings_dict.get("enabled"),
                "fallback_cloud": settings_dict.get("fallback_cloud"),
                "feature_diagnostico_sugerido": features.get("diagnostico_sugerido", True),
                "feature_resumen_clinico": features.get("resumen_clinico", True),
                "feature_ocr_asistido": features.get("ocr_asistido", True),
            }
        )
