import mysql.connector
from typing import List, Optional
from Model.UsuarioModel import UsuarioModel
from configurations import settings
import logging
from Repository.MySqlRepository import MySqlRepository
from fastapi import Depends

logger = logging.getLogger(__name__)

class UsuarioRepository(MySqlRepository):

    #Inicializacion de la conexión
    def __init__(self):
        logger.info("ClienteRepository inicializado")
    
    def crear_usuario(self, usuario: UsuarioModel):
        try:

            conn = self.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM Usuario WHERE identificacion = %s", (usuario.identificacion,))
            existente = cursor.fetchone()
            if existente:
                raise ValueError("El usuario con esa identificación ya existe")

            sql = "INSERT INTO Usuario (identificacion, nombre, correo, celular) VALUES (%s, %s, %s, %s)"
            valores = (usuario.identificacion, usuario.nombre, usuario.correo, usuario.celular)
            cursor.execute(sql, valores)
            conn.commit()
            logger.info(f"Usuario creado con éxito: {usuario.nombre}")
            return True
        except mysql.connector.Error as e:
            logger.error(f"Error al crear el usuario: {e}")
            conn.rollback()
            raise



    def listar_usuarios(self) -> List[UsuarioModel]:
        try:
            conn = self.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM Usuario")
            rows = cursor.fetchall()
            usuarios = [UsuarioModel(**row) for row in rows]
            return usuarios
        except Exception as e:
            logger.exception(f"Error al listar los usuarios {str(e)}")
            return []
        finally:
            cursor.close()
            conn.close()


    def listar_usuario_por_id(self, identificacion: int) -> List[UsuarioModel]:
        try:
            conn = self.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM Usuario WHERE identificacion = %s", (identificacion,))
            rows = cursor.fetchall()

            if not rows:
                raise ValueError(f"No se encontró ningún usuario con la identificación {identificacion}")

            usuario = [UsuarioModel(**row) for row in rows]
            return usuario

        except Exception as e:
            logger.exception(f"Error al listar usuario por ID: {str(e)}")
            raise  # Importante: relanzar la excepción para que la capa superior la maneje
        finally:
            cursor.close()
            conn.close()


    def actualizar_usuario_por_id(self, identificacion: int, datos_actualizados: dict) -> bool:
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            campos = ', '.join(f"{k} = %s" for k in datos_actualizados.keys())
            valores = list(datos_actualizados.values())
            valores.append(identificacion)
            sql = f"UPDATE Usuario SET {campos} WHERE identificacion = %s"
            cursor.execute(sql, valores)
            logger.info(f"SQL: {sql}")
            logger.info(f"Valores: {valores}")
            conn.commit()
            actualizado = cursor.rowcount > 0
            if actualizado:
                logger.info(f"Usuario con ID {identificacion} actualizado")
            else:
                logger.info(f"No se encontró usuario con ID {identificacion} para actualizar")
            return actualizado
        except Exception as e:
            logger.exception(f"Error al actualizar usuario: {str(e)}")
            return False
        finally:
            cursor.close()
            conn.close()

    def asignar_contraseña(self, identificacion: int, contraseña_hasheada: str) -> bool:
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            sql = "UPDATE Usuario SET contraseña = %s WHERE identificacion = %s"
            cursor.execute(sql, (contraseña_hasheada, identificacion))
            conn.commit()
            actualizado = cursor.rowcount > 0
            return actualizado
        except Exception as e:
            logger.exception(f"Error al asignar contraseña: {str(e)}")
            return False
        finally:
            cursor.close()
            conn.close()


    def buscar_usuario(self, identificacion: int) -> UsuarioModel:
        try:
            conn = self.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM Usuario WHERE identificacion = %s", (identificacion,))
            usuario = cursor.fetchone()
            return usuario
        except Exception as e:
            logger.exception(f"Error al buscar usuario por identificacion: {str(e)}")
            return None
        finally:
            cursor.close()
            conn.close()


    def actualizar_rol(self, identificacion: int, nuevo_rol: str) -> bool:
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            sql = "UPDATE Usuario SET rol = %s WHERE id_pedido = %s"
            cursor.execute(sql, (nuevo_rol, identificacion))
            conn.commit()
            return cursor.rowcount > 0 
        except Exception as e:
            logger.exception(f"Error al actualizar el rol del usuario: {str(e)}")
            return False
        finally:
            cursor.close()
            conn.close()



