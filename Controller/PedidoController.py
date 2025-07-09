from fastapi import APIRouter, HTTPException
from Service.PedidoServiceImp import PedidoServiceImp
from Model.PedidoModel import PedidoModel
from fastapi import Depends
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
            raise HTTPException(status_code=500, detail="Erro en el servicio")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al crear el pedido")