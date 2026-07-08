from decimal import Decimal


def get_predictiva_config(institucion):
    defaults = {
        "ausentismo_umbral_alto": 70,
        "ausentismo_umbral_medio": 40,
        "habilitar_ausentismo": True,
        "habilitar_demanda": True,
        "habilitar_riesgo_cronico": True,
    }
    if not institucion:
        return defaults
    cfg = institucion.configuracion.get("predictiva", {}) if isinstance(institucion.configuracion, dict) else {}
    return {**defaults, **cfg}


def nivel_desde_probabilidad(probabilidad, config):
    prob = float(probabilidad)
    if prob >= config["ausentismo_umbral_alto"]:
        return "alto"
    if prob >= config["ausentismo_umbral_medio"]:
        return "medio"
    return "bajo"
