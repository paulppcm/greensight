"""Decisiones automáticas de GreenSight; no realiza operaciones de hardware."""

import config


def controlar_luz(luz):
    if luz <= config.LUZ_MUY_BAJA:
        return {
            "estado_luz": "MUY BAJA",
            "led": True,
            "alerta_luz": "CRITICA",
        }
    if luz <= config.LUZ_BAJA:
        return {
            "estado_luz": "BAJA",
            "led": True,
            "alerta_luz": "BAJA",
        }
    return {
        "estado_luz": "NORMAL",
        "led": False,
        "alerta_luz": None,
    }


def controlar_temperatura(temperatura):
    if temperatura is None:
        return {
            "estado_temperatura": "SIN DATO",
            "ventilador": False,
            "alerta_temperatura": "LECTURA INVALIDA",
        }

    if temperatura >= config.TEMPERATURA_MAX:
        return {
            "estado_temperatura": "ALTA",
            "ventilador": True,
            "alerta_temperatura": "ALTA",
        }

    return {
        "estado_temperatura": "NORMAL",
        "ventilador": False,
        "alerta_temperatura": None,
    }


def controlar_humedad_suelo(humedad_suelo):
    if humedad_suelo <= config.HUMEDAD_SUELO_MIN:
        return {
            "estado_suelo": "SECO",
            "bomba": True,
            "alerta_suelo": "BAJA",
        }

    return {
        "estado_suelo": "NORMAL",
        "bomba": False,
        "alerta_suelo": None,
    }


def aplicar_control(datos):
    estado = {}
    estado.update(controlar_luz(datos["luz"]))
    estado.update(controlar_temperatura(datos["temperatura"]))
    estado.update(controlar_humedad_suelo(datos["humedad_suelo"]))
    return estado
