"""Configuración de GreenSight. Los valores de calibración son provisionales."""

PUERTO_SUELO = 0
PUERTO_LUZ = 2
PUERTO_LED = 4
PUERTO_DHT = 7
TIPO_DHT = 0  # DHT11

# Configurar estos puertos cuando bomba y ventilador estén conectados al GrovePi.
PUERTO_BOMBA = None
PUERTO_VENTILADOR = None

# 1 significa que el actuador se enciende escribiendo HIGH.
# Cambiar a 0 si el módulo relé utilizado trabaja con lógica activa en LOW.
NIVEL_ACTIVO_BOMBA = 1
NIVEL_ACTIVO_VENTILADOR = 1

VALOR_SUELO_SECO = 800
VALOR_SUELO_HUMEDO = 300

LUZ_MUY_BAJA = 100
LUZ_BAJA = 300

# Parámetros iniciales de control. Más adelante podrán venir desde la app.
TEMPERATURA_MAX = 28
HUMEDAD_SUELO_MIN = 40

TIEMPO_ACTUALIZACION = 3

BUS_I2C = 1
LCD_ADDR = 0x3E
RGB_ADDR = 0x30
CARACTERES_LCD = 16
