# greensight
Proyecto II 

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
`/estado` informa la decisión de control sin accionar actuadores.
Detener el servidor con `Ctrl+C`.
