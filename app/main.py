from fastapi import FastAPI
from app.routers.alumno import router as router_alumno
from app.routers.carrera import router as router_carrera
from app.routers.docente import router as router_docente
from app.db.database import Base, engine

app = FastAPI()


app.include_router(router_alumno)
app.include_router(router_carrera)
app.include_router(router_docente)


Base.metadata.create_all(bind=engine)
