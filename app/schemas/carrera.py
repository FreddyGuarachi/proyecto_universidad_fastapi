from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from app.schemas.common import AlumnoSimple, DocenteSimple


class CarreraBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1, max_length=100)
    titulo_otorgado: str = Field(..., min_length=1, max_length=50)
    cantidad_materias: int = Field(..., ge=1, le=70)


class CarreraCreate(CarreraBase):
    pass


class CarreraUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, min_length=1, max_length=100)
    titulo_otorgado: Optional[str] = Field(None, min_length=1, max_length=50)
    cantidad_materias: Optional[int] = Field(None, ge=1, le=70)


class CarreraResponse(CarreraBase):
    id: int
    alumnos: list[AlumnoSimple]
    docentes: list[DocenteSimple]
    model_config = ConfigDict(from_attributes=True)


class CarreraListResponse(BaseModel):
    items: list[CarreraResponse]
    total: int
