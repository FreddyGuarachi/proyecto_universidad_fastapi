from fastapi import FastAPI

from .alumno_router import router as alumno_router
from .docente_router import router as docente_router
from .carrera import router as carrera_router


def register_routers(app: FastAPI):
    app.include_router(alumno_router)
    app.include_router(docente_router)
    app.include_router(carrera_router)
