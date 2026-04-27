# app/schemas.py
from pydantic import BaseModel

# Esquema para crear una estación
class EstacionCreate(BaseModel):
    id: int
    nombre: str
    ubicacion: str

# Esquema para registrar una lectura
class LecturaCreate(BaseModel):
    estacion_id: int
    valor: float