# greensight
Proyecto II

## Control automático

GreenSight analiza las lecturas de los sensores y genera tres decisiones:

- luminosidad baja -> encender LED;
- temperatura alta -> encender ventilador;
- humedad de suelo baja -> encender bomba.

Los valores iniciales de control están en `config.py`:

- `LUZ_MUY_BAJA`
- `LUZ_BAJA`
- `TEMPERATURA_MAX`
- `HUMEDAD_SUELO_MIN`

Conexiones configuradas en GrovePi:

- bomba de agua / relé -> D2 (`PUERTO_BOMBA = 2`)
- ventilador / módulo de control -> D3 (`PUERTO_VENTILADOR = 3`)
- LED -> D4
- DHT11 -> D7


Si un relé se activa con nivel LOW, cambiar su valor `NIVEL_ACTIVO_...` de `1` a `0`.

Ejecutar el sistema:

```bash
python3 main.py
```

Probar solo la lógica de control, sin hardware:

```bash
python3 -m unittest test_control.py
```

## API local

Instalar desde la carpeta del proyecto en la Raspberry:

```bash
python3 -m pip install -r requirements.txt
```

Ejecutar:

```bash
python3 -m uvicorn api:app --host 0.0.0.0 --port 8000
```

Consultar desde otro dispositivo conectado a la misma red WiFi:

- `http://IP_DE_LA_RASPBERRY:8000/`
- `http://IP_DE_LA_RASPBERRY:8000/sensores`
- `http://IP_DE_LA_RASPBERRY:8000/estado`
- `http://IP_DE_LA_RASPBERRY:8000/docs`

Para conocer la IP de la Raspberry, ejecutar `hostname -I` y usar su dirección WiFi.

`/estado` informa las decisiones de control sin accionar actuadores.

Detener el servidor con `Ctrl+C`.
