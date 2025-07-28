from Service.INotificacionService import INotificacionService
from Repository.NotificacionRepository import NotificacionRepository
from Model.NotificacionModel import NotificacionModel
from fastapi import Depends
from typing import List
import logging


logger = logging.getLogger(__name__)

class NotificacionServiceImp(INotificacionService):
    def __init__(self, repo: NotificacionRepository = Depends()):
        self.repo = repo

    def crear_notificacion(self, notificacion: NotificacionModel) -> NotificacionModel:
        try:
            if not notificacion:
                logger.warning("Notificacion invalida: objeto vacío o nulo")
                raise ValueError("la notificacion no puede ser nulo")

            if not notificacion.usuario_id:
                logger.warning("Notificacion invalida: falta la identificacion del cliente")
                raise ValueError("la identificacion es obligatoria para crear la notificacion")

            creada = self.repo.crear_notificacion(notificacion)
            if creada:
                logger.info(f"Notificacion creada correctamente: {creada}")
                return creada
            else:
                logger.error("No se pudo crear la notificacion en el repositorio")
                raise Exception("Error interno al guardar la notificacion")

        except Exception as e:
            logger.exception(f"Error al crear la notificacion: {str(e)}")
            raise e


    def listar_notificaciones(self) -> List[NotificacionModel]:
        try:
            notificaciones = self.repo.listar_notificaciones()
            if notificaciones:
                logger.info(f"Se listaron {len(notificaciones)} notificaciones correctamente")
                return notificaciones
            else:
                logger.info("No se encontraron notificaciones")
                return []
        except Exception as e:
            logger.exception(f"Error al listar notificaciones: {str(e)}")
            raise e


    def listar_mis_notificaciones(self, usuario_id: int) -> List[NotificacionModel]:
        try:
            if not usuario_id:
                logger.warning("Identificacion del cliente no proporcionada para listar los pedidos")
                raise ValueError("La identificación es obligatoria")
            notificaciones = self.repo.listar_mis_notificaciones(usuario_id)
            if notificaciones:
                logger.info(f"Se listaron {len(notificaciones)} pedidos del cliente {usuario_id}")
                return notificaciones
            else:
                logger.info(f"No se encontraron notificaciones para el cliente {usuario_id}")
                return []
        except Exception as e:
            logger.exception(f"Error al listar notificaciones del cliente: {str(e)}")
            raise e