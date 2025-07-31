from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class NotificacionModel(BaseModel):
    id_notificacion: Optional[int] = None
    usuario_id: int
    pedido_id: int
    mensaje: str
    fecha: datetime
