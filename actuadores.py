"""Manejo del LED. Los futuros actuadores se agregarán en este módulo."""

import grovepi

import config


def inicializar_actuadores():
    grovepi.pinMode(config.PUERTO_LED, "OUTPUT")
    apagar_todo()


def encender_led():
    grovepi.digitalWrite(config.PUERTO_LED, 1)


def apagar_led():
    grovepi.digitalWrite(config.PUERTO_LED, 0)


def controlar_led(encendido):
    if encendido:
        encender_led()
    else:
        apagar_led()


def apagar_todo():
    apagar_led()
