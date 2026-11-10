"""Decisiones automáticas; no realiza operaciones de hardware."""

import config


def controlar_luz(luz):
    if luz <= config.LUZ_MUY_BAJA:
        return {"estado_luz": "MUY BAJA", "led": True, "alerta_luz": "CRITICA"}
    if luz <= config.LUZ_BAJA:
        return {"estado_luz": "BAJA", "led": True, "alerta_luz": "BAJA"}
    return {"estado_luz": "NORMAL", "led": False, "alerta_luz": None}


def aplicar_control(datos):
    luz = datos["luz"]
    estado = controlar_luz(luz)
    # Las futuras decisiones se incorporarán al mismo diccionario.
    return estado
