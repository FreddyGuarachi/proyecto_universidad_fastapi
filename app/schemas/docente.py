from pydantic import BaseModel, Field, EmailStr, ConfigDict
from typing import Optional
from app.schemas.common import CarreraSimple


class DocenteBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    matricula: str = Field(..., min_length=1, max_length=50)
    dni: str = Field(..., min_length=1, max_length=50)
    phone_number: str = Field(..., min_length=1, max_length=20)
    email: EmailStr
    address: str = Field(..., min_length=1, max_length=100)


class DocenteCreate(DocenteBase):
    carrera_id: int = Field(..., ge=1)


class DocenteUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    matricula: Optional[str] = Field(None, min_length=1, max_length=50)
    dni: Optional[str] = Field(None, min_length=1, max_length=50)
    phone_number: Optional[str] = Field(None, min_length=1, max_length=20)
    email: Optional[EmailStr] = None
    address: Optional[str] = Field(None, min_length=1, max_length=100)
    carrera_id: Optional[int] = Field(None, ge=1)


class DocenteResponse(DocenteBase):
    id: int
    carrera: CarreraSimple
    model_config = ConfigDict(from_attributes=True)


class DocenteListResponse(BaseModel):
    items: list[DocenteResponse]
    total: int
