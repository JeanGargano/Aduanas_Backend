import mysql.connector
from typing import List, Optional
from Model.NotificacionModel import NotificacionModel
from configurations import settings
import logging
from Repository.MySqlRepository import MySqlRepository
from fastapi import Depends

logger = logging.getLogger(__name__)

class NotificacionRepository(MySqlRepository):

    #Inicializacion de la conexión
    def __init__(self):
        logger.info("Notificacion Repository inicializado")
    
    def crear_notificacion(self, notificacion: NotificacionModel) -> NotificacionModel:
        try:
            conn = self.get_connection()
            cursor = conn.cursor(dictionary=True)
            sql = "INSERT INTO Notificacion (usuario_id, pedido_id, mensaje) VALUES (%s, %s, %s)"
            valores = (notificacion.usuario_id, notificacion.pedido_id, notificacion.mensaje)
            cursor.execute(sql, valores)
            conn.commit()
            notificacion.id_notificacion = cursor.lastrowid  #asignamos el ID generado
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
            cursor.execute("SELECT * FROM Notificacion")
            rows = cursor.fetchall()
            notificaciones = [NotificacionModel(**row) for row in rows]
            return notificaciones
        except Exception as e:
            logger.exception(f"Error al listar las notificaciones {str(e)}")
            return []
        finally:
            cursor.close()
            conn.close()

    def listar_mis_notificaciones(self, usuario_id: int):
        try:
            conn = self.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM Notificacion WHERE usuario_id = %s", (usuario_id, ))
            rows = cursor.fetchall()
            usuarios = [NotificacionModel(**row) for row in rows]
            return usuarios
        except Exception as e:
            logger.exception(f"Error al listar las notificaciones {str(e)}")
            return []
        finally:
            cursor.close()
            conn.close()