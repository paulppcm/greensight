"""API local para consultar los sensores y las decisiones de GreenSight."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

import sensores
import control


@asynccontextmanager
async def iniciar_api(app):
    """Prepara las entradas de los sensores antes de recibir peticiones."""
    sensores.inicializar_sensores()
    yield


app = FastAPI(lifespan=iniciar_api)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.get("/")
def inicio():
    return {"sistema": "GreenSight", "estado": "activo"}


@app.get("/sensores")
def obtener_sensores():
    try:
        datos = sensores.leer_sensores()
    except Exception:
        return JSONResponse(
            status_code=503,
            content={"error": "No se pudieron leer los sensores"},
        )
    return datos


@app.get("/estado")
def obtener_estado():
    try:
        datos = sensores.leer_sensores()
    except Exception:
        return JSONResponse(
            status_code=503,
            content={"error": "No se pudieron leer los sensores"},
        )
    decision = control.aplicar_control(datos)
    return {"datos": datos, "control": decision}
