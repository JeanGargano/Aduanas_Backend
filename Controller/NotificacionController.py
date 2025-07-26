from fastapi import APIRouter, HTTPException
from Service.NotificacionServiceImp import NotificacionServiceImp
from Model.NotificacionModel import NotificacionModel
from fastapi import Depends, Query
router = APIRouter()

@router.post("/crear_notificacion")
def crear_notificacion(
    notificacion: NotificacionModel,
    service: NotificacionServiceImp = Depends()
):
    try:
        res = service.crear_notificacion(notificacion)
        if res:
            return res
        else:
            raise HTTPException(status_code=500, detail="Error en el servicio")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al crear la notificacion")
    
    
@router.get("/listar_notificaciones")
def listar_notificaciones(
    service: NotificacionServiceImp = Depends()
):
    try:
        res = service.listar_notificaciones()
        if res:
            return res
        else:
            raise HTTPException(status_code=500, detail="Error en el servicio")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al listar las notificaciones")
    
    
@router.get("/listar_mis_notificaciones")
def listar_mis_notificaciones(
    usuario_id: int = Query(...),
    service: NotificacionServiceImp = Depends()
):
    try:
        return service.listar_mis_notificaciones(usuario_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")
    