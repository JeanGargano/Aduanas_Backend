from pydantic import BaseModel
from typing import Optional

class UsuarioModel(BaseModel):
    identificacion: int
    nombre: str
    correo: str
    celular: int
    rol: Optional[str]
    contraseña: Optional[str] = ""
