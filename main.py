"""Punto de entrada y coordinación de GreenSight."""

import time

import actuadores
import config
import control
import lcd
import sensores


def mostrar_terminal(datos, estado):
    temperatura = datos["temperatura"]
    humedad = datos["humedad_aire"]
    if temperatura is None:
        temperatura = "N/D"
    if humedad is None:
        humedad = "N/D"
    texto_led = "APAGADO"
    if estado["led"]:
        texto_led = "ENCENDIDO"
    print("------- GreenSight -------")
    print(f"Temperatura: {temperatura} C")
    print(f"Humedad ambiente: {humedad} %")
    print(f"Valor suelo RAW: {datos['valor_suelo']}")
    print(f"Humedad suelo: {datos['humedad_suelo']} %")
    print(f"Nivel de luz: {datos['luz']}")
    print(f"Estado luz: {estado['estado_luz']}")
    print(f"LED: {texto_led}")
    print("--------------------------")


def detener_sistema(error=None):
    """Intenta cada acción de cierre aunque otro dispositivo falle."""
    try:
        actuadores.apagar_todo()
    except Exception as fallo:
        print(f"No se pudieron apagar los actuadores: {fallo}")

    try:
        if lcd.bus is not None:
            if error is None:
                lcd.cambiar_color(0, 0, 0)
                lcd.escribir_lcd("Sistema detenido", "")
            else:
                lcd.cambiar_color(255, 0, 0)
                lcd.escribir_lcd("ERROR", "Revisar sistema")
    except Exception as fallo:
        print(f"No se pudo actualizar la LCD: {fallo}")
    finally:
        if lcd.bus is not None:
            try:
                lcd.bus.close()
            except Exception as fallo:
                print(f"No se pudo cerrar el bus I2C: {fallo}")
            lcd.bus = None


def main():
    try:
        actuadores.inicializar_actuadores()
        sensores.inicializar_sensores()
        lcd.inicializar_lcd()
        pantalla = 0

        while True:
            datos = sensores.leer_sensores()
            estado = control.aplicar_control(datos)
            actuadores.controlar_led(estado["led"])
            lcd.mostrar_estado(datos, estado, pantalla)
            mostrar_terminal(datos, estado)
            pantalla = (pantalla + 1) % 3
            time.sleep(config.TIEMPO_ACTUALIZACION)

    except KeyboardInterrupt:
        detener_sistema()
        print("Sistema detenido")
    except Exception as error:
        print(f"Error en GreenSight: {error}")
        detener_sistema(error)


if __name__ == "__main__":
    main()
