from fastapi import APIRouter, HTTPException
from app.Service.PedidoServiceImp import PedidoServiceImp
from app.Model.PedidoModel import PedidoModel
from fastapi import Depends, Query, Body
router = APIRouter()

@router.post("/crear_pedido")
def crear_pedido(
    pedido: PedidoModel,
    service: PedidoServiceImp = Depends()
):
    try:
        res = service.crear_pedido(pedido)
        if res:
            return {f"Pedido creado exitosamente"}
        else:
            raise HTTPException(status_code=500, detail="Error en el servicio")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al crear el pedido")
    
    
@router.get("/listar_pedidos")
def listar_pedidos(
    service: PedidoServiceImp = Depends()
):
    try:
        res = service.listar_pedidos()
        if res:
            return res
        else:
            raise HTTPException(status_code=500, detail="Error en el servicio")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al listar los pedidos")
    
    
@router.get("/listar_pedidos_del_cliente")
def listar_pedidos_del_cliente(
    id_cliente: int = Query(...),
    service: PedidoServiceImp = Depends()
):
    try:
        return service.listar_pedidos_del_cliente(id_cliente)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")
    

@router.get("/listar_pedido_por_id")
def listar_pedido_por_id(
    id_pedido: int = Query(...),
    service: PedidoServiceImp = Depends()
):
    try:
        return service.listar_pedido_por_id(id_pedido)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")
    

    
@router.put("/actualizar_pedido_por_id")
def actualizar_pedido_por_id(
    id_pedido: int = Query(...),
    datos_actualizados: dict = Body(...),
    service: PedidoServiceImp = Depends()
):
    try:
        actualizado = service.actualizar_pedido_por_id(id_pedido, datos_actualizados)
        if not actualizado:
            raise HTTPException(status_code=404, detail="Pedido no encontrado")
        return {"message": "Pedido actualizado correctamente"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Error interno al actualizar el pedido")
    
