from pydantic import BaseModel
from typing import Optional

class ClienteModel(BaseModel):
    identificacion: int
    nombre: str
    correo: str
    celular: int
    rol: Optional[str] = "Cliente"
    contraseña: str
