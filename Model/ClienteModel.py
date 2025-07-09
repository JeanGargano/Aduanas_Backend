from pydantic import BaseModel
from typing import Optional

class Cliente(BaseModel):
    identificacion: int
    nombre: str
    correo: str
    celular: int
    rol: Optional[str] = "Cliente"
