"""Lectura de sensores y conversión de sus mediciones."""

import math

import grovepi

import config


def inicializar_sensores():
    grovepi.pinMode(config.PUERTO_SUELO, "INPUT")
    grovepi.pinMode(config.PUERTO_LUZ, "INPUT")
    # grovepi.dht configura la lectura digital del DHT11.


def calcular_humedad_suelo(valor):
    rango = config.VALOR_SUELO_SECO - config.VALOR_SUELO_HUMEDO
    if rango == 0:
        raise ValueError("La calibración seca y húmeda debe ser diferente")
    porcentaje = (config.VALOR_SUELO_SECO - valor) * 100 / rango
    return round(max(0, min(100, porcentaje)), 1)


def leer_dht():
    """Devuelve (temperatura, humedad); ambas son None si falla la lectura."""
    try:
        temperatura, humedad = grovepi.dht(config.PUERTO_DHT, config.TIPO_DHT)
        if temperatura == -1 or humedad == -1:
            return None, None
        if not math.isfinite(temperatura) or not math.isfinite(humedad):
            return None, None
        return temperatura, humedad
    except Exception:
        # Un fallo del DHT no impide leer los demás sensores.
        return None, None


def leer_sensores():
    temperatura, humedad_aire = leer_dht()
    valor_suelo = grovepi.analogRead(config.PUERTO_SUELO)
    luz = grovepi.analogRead(config.PUERTO_LUZ)
    humedad_suelo = calcular_humedad_suelo(valor_suelo)
    return {
        "temperatura": temperatura,
        "humedad_aire": humedad_aire,
        "valor_suelo": valor_suelo,
        "humedad_suelo": humedad_suelo,
        "luz": luz,
    }
