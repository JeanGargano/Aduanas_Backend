from fastapi import APIRouter, HTTPException
import logging
from Service.UsuarioServiceImp import UsuarioServiceImp
from Model.UsuarioModel import UsuarioModel
from mysql.connector.errors import IntegrityError
from fastapi import Depends, Query, Body
router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/crear_usuario")
def crear_usuario(
    usuario: UsuarioModel,
    service: UsuarioServiceImp = Depends()
):
    try:
        res = service.crear_usuario(usuario)
        if res:
            return {"message": "Usuario creado exitosamente"}
        else:
            raise HTTPException(status_code=500, detail="Error en el servicio")
    except IntegrityError as e:
        if "Duplicate entry" in str(e):
            raise HTTPException(status_code=400, detail="El usuario ya existe en el sistema")
        raise HTTPException(status_code=400, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error inesperado al crear el usuario")
    
    
@router.get("/listar_usuarios")
def listar_usuarios(
    service: UsuarioServiceImp = Depends()
):
    try:
        res = service.listar_usuarios()
        if res:
            return res
        else:
            raise HTTPException(status_code=500, detail="Error en el servicio")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al listar los pedidos")
    
    
@router.get("/listar_usuario_por_id")
def listar_usuario_por_id(
    identificacion: int = Query(...),
    service: UsuarioServiceImp = Depends()
):
    try:
        return service.listar_usuario_por_id(identificacion)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")
    
    
    
@router.put("/actualizar_usuario_por_id")
def actualizar_usuario_por_id(
    identificacion: int = Query(...),
    datos_actualizados: dict = Body(...),
    service: UsuarioServiceImp = Depends()
):
    try:
        actualizado = service.actualizar_usuario_por_id(identificacion, datos_actualizados)
        if not actualizado:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return {"message": "Usuario actualizado correctamente"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Error interno al actualizar el usuario")
    
@router.put("/asignar_contraseña")
def asignar_contraseña(
    data: dict = Body(...),
    service: UsuarioServiceImp = Depends()
):
    try:
        identificacion = data["identificacion"]
        contraseña = data["contraseña"]
        asignado = service.asignar_contraseña(identificacion, contraseña)
        if not asignado:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return {"message": "Contraseña asignada exitosamente"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Error interno al añadir la contraseña")
    

@router.post("/logear_usuario")
def logear_usuario(
    data: dict = Body(...),
    service: UsuarioServiceImp = Depends()
):
    try:
        identificacion = data["identificacion"]
        contraseña = data["contraseña"]
        usuario = service.logear_usuario(identificacion, contraseña)
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return usuario
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Error interno al logear el usuario")
      
    
