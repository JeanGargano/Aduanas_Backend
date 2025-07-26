from Model.NotificacionModel import NotificacionModel
from abc import abstractmethod, ABC
from typing import List

class INotificacionService(ABC):

    @abstractmethod
    def crear_notificacion(self, notificacion: NotificacionModel) -> NotificacionModel:
        pass

    @abstractmethod
    def listar_notificaciones(self) -> List[NotificacionModel]:
        pass

    @abstractmethod
    def listar_mis_notificaciones(self, usuario_id: int) -> List[NotificacionModel]:
        pass


