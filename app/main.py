from fastapi import FastAPI
from app.routers.alumno import router as router_alumno
from app.routers.carrera import router as router_carrera
from app.routers.docente import router as router_docente
from app.db.database import Base, engine
from app.auth.router import router as router_auth
from app.middlewares.cors import configurar_cors
from app.middlewares.time_header import configurar_time_header


def create_app():

    app = FastAPI()
    configurar_cors(app)
    configurar_time_header(app)
    app.include_router(router_alumno)
    app.include_router(router_carrera)
    app.include_router(router_docente)
    app.include_router(router_auth)

    Base.metadata.create_all(bind=engine)

    return app


app = create_app()
