from pydantic import BaseModel
from typing import Optional

class NotificacionModel(BaseModel):
    id_notificacion: Optional[int] = None
    usuario_id: int
    pedido_id: int
    mensaje: str
