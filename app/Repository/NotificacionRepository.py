import mysql.connector
from typing import List
from app.Model.NotificacionModel import NotificacionModel
import logging
from app.Repository.MySqlRepository import MySqlRepository

logger = logging.getLogger(__name__)

class NotificacionRepository(MySqlRepository):

    def __init__(self):
        super().__init__()
    
    def crear_notificacion(self, notificacion: NotificacionModel) -> NotificacionModel:
        try:
            conn = self.get_connection()
            cursor = conn.cursor(dictionary=True)
            sql = "INSERT INTO notificacion (usuario_id, pedido_id, mensaje, fecha) VALUES (%s, %s, %s, %s)"
            valores = (notificacion.usuario_id, notificacion.pedido_id, notificacion.mensaje, notificacion.fecha)
            cursor.execute(sql, valores)
            conn.commit()
            notificacion.id_notificacion = cursor.lastrowid 
            logger.info(f"Notificacion creada con éxito")
            return notificacion
        except mysql.connector.Error as e:
            logger.error(f"Error al crear la notificacion: {e}")
            conn.rollback()
            raise



    def listar_notificaciones(self) -> List[NotificacionModel]:
        try:
            conn = self.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM notificacion")
            rows = cursor.fetchall()
            notificaciones = [NotificacionModel(**row) for row in rows]
            return notificaciones
        except Exception as e:
            logger.exception(f"Error al listar las notificaciones {str(e)}")
            return []
        finally:
            cursor.close()
            conn.close()

    def listar_mis_notificaciones(self, usuario_id: int) ->List[NotificacionModel]:
        try:
            conn = self.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM notificacion WHERE usuario_id = %s", (usuario_id, ))
            rows = cursor.fetchall()
            usuarios = [NotificacionModel(**row) for row in rows]
            return usuarios
        except Exception as e:
            logger.exception(f"Error al listar las notificaciones {str(e)}")
            return []
        finally:
            cursor.close()
            conn.close()