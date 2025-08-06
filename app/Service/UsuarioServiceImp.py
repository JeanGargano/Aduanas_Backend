from app.Service.IUsuarioService import IUsuarioService
from app.Repository.UsuarioRepository import UsuarioRepository
from app.Model.UsuarioModel import UsuarioModel
from typing import List
from fastapi import Depends
import bcrypt
import logging 
from app.Service.AutenticacionUtil import crear_access_token
from datetime import timedelta

logger = logging.getLogger(__name__)


def verificar_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


class UsuarioServiceImp(IUsuarioService):
    def __init__(self, repo: UsuarioRepository = Depends()):
        self.repo = repo

    def crear_usuario(self, usuario: UsuarioModel) -> str:
        try:
            if not usuario or not usuario.nombre or not usuario.identificacion or not usuario.correo:
                raise ValueError("Datos de usuario incompletos o inválidos.")

            usuario_existente = self.repo.buscar_usuario(usuario.identificacion)
            if usuario_existente:
                raise ValueError("El usuario con esa identificación ya existe.")

            self.repo.crear_usuario(usuario)
            return "Usuario creado exitosamente"
        except Exception as e:
            logger.error(f"Error al crear usuario: {e}")
            raise

    def listar_usuarios(self) -> List[UsuarioModel]:
        try:
            usuarios = self.repo.listar_usuarios()
            logger.info("Listado de usuarios obtenido correctamente")
            return usuarios
        except Exception as e:
            logger.error(f"Error al listar usuarios: {e}")
            raise

    def listar_usuario_por_id(self, identificacion: int) -> List[UsuarioModel]:
        try:
            if identificacion <= 0:
                raise ValueError("Identificación inválida")
            usuario = self.repo.listar_usuario_por_id(identificacion)
            if not usuario:
                logger.warning(f"No se encontró usuario con ID {identificacion}")
            return usuario
        except Exception as e:
            logger.error(f"Error al buscar usuario por ID: {e}")
            raise

    def actualizar_usuario_por_id(self, identificacion: int, datos_actualizados: dict) -> bool:
        try:
            if not datos_actualizados:
                raise ValueError("Los datos no pueden estar vacíos")
            actualizado = self.repo.actualizar_usuario_por_id(identificacion, datos_actualizados)
            if actualizado:
                logger.info(f"Usuario con ID {identificacion} actualizado correctamente")
            else:
                logger.warning(f"No se pudo actualizar usuario con ID {identificacion}")
            return actualizado
        except Exception as e:
            logger.error(f"Error al actualizar usuario: {e}")
            raise

    def asignar_contraseña(self, identificacion: int, contraseña: str) -> bool:
        try:
            if not contraseña:
                raise ValueError("Debe incluir la contraseña")
            usuario = self.repo.buscar_usuario(identificacion)
            if not usuario:
                raise ValueError("Usuario no encontrado")
            hashed = bcrypt.hashpw(contraseña.encode('utf-8'), bcrypt.gensalt())
            actualizado = self.repo.asignar_contraseña(identificacion, hashed.decode('utf-8'))
            if actualizado:
                logger.info(f"Contraseña asignada correctamente al usuario con ID {identificacion}")
            else:
                logger.warning(f"No se pudo asignar contraseña al usuario con ID {identificacion}")
            return actualizado
        except Exception as e:
            logger.error(f"Error al asignar contraseña: {e}")
            raise


    def autenticar_usuario(self, identificacion: int, password: str):
        usuario = self.repo.buscar_usuario(identificacion)
        if not usuario:
            return None
        if not verificar_password(password, usuario["contraseña"]):
            return None
        return usuario

    def crear_token_para_usuario(self, identificacion: int):
        access_token = crear_access_token({"sub": str(identificacion)})
        return access_token



