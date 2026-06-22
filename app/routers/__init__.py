from fastapi import FastAPI

from .alumno_router import router as alumno_router
from .docente_router import router as docente_router
from .carrera_router import router as carrera_router
from .user_router import router as user_router


def register_routers(app: FastAPI):
    app.include_router(alumno_router)
    app.include_router(docente_router)
    app.include_router(carrera_router)
    app.include_router(user_router)
