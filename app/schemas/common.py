from pydantic import BaseModel, ConfigDict


class CarreraSimple(BaseModel):
    id: int
    name: str
    model_config = ConfigDict(from_attributes=True)


class AlumnoSimple(BaseModel):
    id: int
    name: str
    model_config = ConfigDict(from_attributes=True)


class DocenteSimple(BaseModel):
    id: int
    name: str
    model_config = ConfigDict(from_attributes=True)
