from fastapi import APIRouter, HTTPException, status
import logging
from app.Service.UsuarioServiceImp import UsuarioServiceImp
from app.Model.UsuarioModel import UsuarioModel
from mysql.connector.errors import IntegrityError
from fastapi.security import OAuth2PasswordRequestForm
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
    

@router.post("/autenticar_usuario")
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    service: UsuarioServiceImp = Depends()
):
    try:
        identificacion = int(form_data.username)
    except ValueError:
        raise HTTPException(status_code=400, detail="Identificación inválida")

    user = service.autenticar_usuario(identificacion, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Identificación o contraseña incorrectas",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = service.crear_token_para_usuario(identificacion)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "usuario": {
            "identificacion": user["identificacion"],
            "nombre": user["nombre"],
            "correo": user["correo"],
            "celular": user["celular"]
        }
    }
    
