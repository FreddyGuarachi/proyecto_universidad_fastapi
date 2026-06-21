from fastapi import FastAPI

from app.routers import register_routers
from app.db.database import Base, engine
from app.auth.router import router as router_auth
from app.middlewares.cors import configurar_cors
from app.middlewares.time_header import configurar_time_header


def create_app():
    app = FastAPI()

    configurar_cors(app)
    configurar_time_header(app)

    register_routers(app)

    app.include_router(router_auth)

    Base.metadata.create_all(bind=engine)

    return app


app = create_app()
