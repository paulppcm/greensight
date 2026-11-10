"""Pantalla Grove LCD RGB Backlight V5.0 de dos líneas."""

import time

import smbus

from config import BUS_I2C, CARACTERES_LCD, LCD_ADDR, RGB_ADDR


# Abrir el bus solo al inicializar, nunca al importar el módulo.
bus = None


def comando(valor):
    bus.write_byte_data(LCD_ADDR, 0x80, valor)
    if valor in (0x01, 0x02):
        time.sleep(0.002)
    else:
        time.sleep(0.00005)


def inicializar_lcd():
    global bus
    bus = smbus.SMBus(BUS_I2C)
    time.sleep(0.05)
    comando(0x28)  # Dos líneas y caracteres de 5x8 puntos.
    time.sleep(0.005)
    comando(0x28)
    time.sleep(0.0002)
    comando(0x28)
    comando(0x0C)  # Pantalla encendida, sin cursor.
    comando(0x01)  # Limpiar pantalla.
    comando(0x06)  # Avanzar el cursor al escribir.

    # Registros del controlador SGM31323 de la versión V5.0.
    bus.write_byte_data(RGB_ADDR, 0x00, 0x07)
    time.sleep(0.0002)
    bus.write_byte_data(RGB_ADDR, 0x04, 0x15)
    cambiar_color(0, 255, 255)


def cambiar_color(r, g, b):
    bus.write_byte_data(RGB_ADDR, 0x06, r)
    bus.write_byte_data(RGB_ADDR, 0x07, g)
    bus.write_byte_data(RGB_ADDR, 0x08, b)


def escribir_lcd(linea1, linea2):
    for direccion, texto in ((0x80, linea1), (0xC0, linea2)):
        comando(direccion)
        # Rellenar con espacios elimina los restos del mensaje anterior.
        texto = str(texto)[:CARACTERES_LCD].ljust(CARACTERES_LCD)
        for caracter in texto:
            bus.write_byte_data(LCD_ADDR, 0x40, ord(caracter))
            time.sleep(0.00005)


def mostrar_estado(datos, estado, pantalla):
    alerta = estado["alerta_luz"]
    if alerta == "CRITICA":
        cambiar_color(255, 0, 0)
        escribir_lcd("ALERTA LUZ", "LED ENCENDIDO")
    elif alerta == "BAJA":
        cambiar_color(255, 255, 0)
        escribir_lcd(f"Luz: {datos['luz']}", "LED ENCENDIDO")
    elif pantalla == 0:
        temperatura = datos["temperatura"]
        humedad = datos["humedad_aire"]
        if temperatura is None:
            temperatura = "N/D"
        if humedad is None:
            humedad = "N/D"
        cambiar_color(0, 0, 255)
        escribir_lcd(f"Temp: {temperatura} C", f"Hum Aire: {humedad}%")
    elif pantalla == 1:
        cambiar_color(0, 255, 0)
        escribir_lcd(f"Suelo: {datos['humedad_suelo']}%", f"Luz: {datos['luz']}")
    else:
        cambiar_color(0, 255, 255)
        escribir_lcd("GreenSight", "Sistema activo")
