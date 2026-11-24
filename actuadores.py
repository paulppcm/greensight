"""Manejo de los actuadores físicos de GreenSight."""

import grovepi

import config


def _inicializar_salida(puerto):
    if puerto is not None:
        grovepi.pinMode(puerto, "OUTPUT")


def _escribir_salida(puerto, encendido, nivel_activo=1):
    if puerto is None:
        return

    nivel_apagado = 0 if nivel_activo == 1 else 1
    valor = nivel_activo if encendido else nivel_apagado
    grovepi.digitalWrite(puerto, valor)


def inicializar_actuadores():
    _inicializar_salida(config.PUERTO_LED)
    _inicializar_salida(config.PUERTO_BOMBA)
    _inicializar_salida(config.PUERTO_VENTILADOR)
    apagar_todo()


def controlar_led(encendido):
    _escribir_salida(config.PUERTO_LED, encendido)


def controlar_bomba(encendida):
    _escribir_salida(
        config.PUERTO_BOMBA,
        encendida,
        config.NIVEL_ACTIVO_BOMBA,
    )


def controlar_ventilador(encendido):
    _escribir_salida(
        config.PUERTO_VENTILADOR,
        encendido,
        config.NIVEL_ACTIVO_VENTILADOR,
    )


def aplicar_estado(estado):
    controlar_led(estado["led"])

    # Protección física adicional: bomba y ventilador nunca se energizan juntos.
    if estado["ventilador"] and estado["bomba"]:
        controlar_bomba(True)
        controlar_ventilador(False)
        return

    controlar_bomba(estado["bomba"])
    controlar_ventilador(estado["ventilador"])


def apagar_todo():
    controlar_led(False)
    controlar_bomba(False)
    controlar_ventilador(False)
