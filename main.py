"""Punto de entrada y coordinación de GreenSight."""

import re
import sys
import time
from pathlib import Path

import actuadores
import config
import control
import lcd
import sensores


def texto_estado(encendido):
    return "ENCENDIDO" if encendido else "APAGADO"


def mostrar_terminal(datos, estado):
    temperatura = datos["temperatura"]
    humedad = datos["humedad_aire"]

    if temperatura is None:
        temperatura = "N/D"
    if humedad is None:
        humedad = "N/D"

    print("------- GreenSight -------")
    print(f"Temperatura: {temperatura} C")
    print(f"Humedad ambiente: {humedad} %")
    print(f"Valor suelo RAW: {datos['valor_suelo']}")
    print(f"Humedad suelo: {datos['humedad_suelo']} %")
    print(f"Nivel de luz: {datos['luz']}")
    print(f"Estado luz: {estado['estado_luz']}")
    print(f"Estado temperatura: {estado['estado_temperatura']}")
    print(f"Estado suelo: {estado['estado_suelo']}")
    print(f"LED: {texto_estado(estado['led'])}")
    print(f"Ventilador: {texto_estado(estado['ventilador'])}")
    print(f"Bomba: {texto_estado(estado['bomba'])}")
    print("--------------------------")


def tomar_promedio_suelo(cantidad=10, pausa=0.3):
    lecturas = []
    for numero in range(1, cantidad + 1):
        valor = sensores.leer_suelo_raw()
        lecturas.append(valor)
        print(f"Muestra {numero}/{cantidad}: {valor}")
        time.sleep(pausa)
    return round(sum(lecturas) / len(lecturas))


def guardar_calibracion(valor_seco, valor_humedo):
    ruta = Path(__file__).with_name("config.py")
    contenido = ruta.read_text(encoding="utf-8")

    contenido = re.sub(
        r"VALOR_SUELO_SECO\s*=\s*\d+",
        f"VALOR_SUELO_SECO = {valor_seco}",
        contenido,
        count=1,
    )
    contenido = re.sub(
        r"VALOR_SUELO_HUMEDO\s*=\s*\d+",
        f"VALOR_SUELO_HUMEDO = {valor_humedo}",
        contenido,
        count=1,
    )

    ruta.write_text(contenido, encoding="utf-8")


def calibrar_suelo():
    sensores.inicializar_sensores()

    print("=== CALIBRACION SENSOR DE SUELO ===")
    print("Se tomarán 10 muestras para cada estado.")
    print()
    print("1) Deja el sensor en tierra SECA o fuera de tierra.")
    input("Presiona ENTER cuando esté listo...")
    valor_seco = tomar_promedio_suelo()

    print()
    print(f"Promedio SECO: {valor_seco}")
    print()
    print("2) Coloca el sensor en tierra bien HÚMEDA.")
    print("   No sumerjas la electrónica del sensor.")
    input("Presiona ENTER cuando esté listo...")
    valor_humedo = tomar_promedio_suelo()

    print()
    print(f"Promedio HÚMEDO: {valor_humedo}")

    if valor_seco == valor_humedo:
        print("ERROR: los valores seco y húmedo resultaron iguales.")
        print("No se guardó la calibración.")
        return

    if valor_seco < valor_humedo:
        print()
        print("ADVERTENCIA: el valor seco fue menor que el húmedo.")
        print("La fórmula actual de GreenSight espera SECO > HÚMEDO.")
        print("Revisa la posición o el tipo de sensor antes de guardar.")
        return

    guardar_calibracion(valor_seco, valor_humedo)

    print()
    print("Calibración guardada correctamente en config.py:")
    print(f"VALOR_SUELO_SECO = {valor_seco}")
    print(f"VALOR_SUELO_HUMEDO = {valor_humedo}")
    print()
    print("Ahora ejecuta nuevamente: python3 main.py")


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
            actuadores.aplicar_estado(estado)
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
    if "--calibrar-suelo" in sys.argv:
        calibrar_suelo()
    else:
        main()
