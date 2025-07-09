from Service.IPedidoService import IPedidoService
from Repository.PedidoRepository import PedidoRepository
from Model.PedidoModel import PedidoModel
from fastapi import Depends
from typing import List
import logging

logger = logging.getLogger(__name__)

class PedidoServiceImp(IPedidoService):
    def __init__(self, repo: PedidoRepository = Depends()):
        self.repo = repo

    def crear_pedido(self, pedido: PedidoModel) -> str:
        try:
            if not pedido:
                logger.warning("Pedido inválido: objeto vacío o nulo")
                raise ValueError("El pedido no puede ser nulo")

            # Si al menos tiene el campo id_cliente, lo aceptamos:
            if not pedido.id_cliente:
                logger.warning("Pedido inválido: falta id_cliente")
                raise ValueError("id_cliente es obligatorio para crear el pedido")

            creado = self.repo.crear_pedido(pedido)
            if creado:
                logger.info(f"Pedido creado correctamente: {creado}")
                return f"Pedido creado con ID: {creado.id_pedido}"
            else:
                logger.error("No se pudo crear el pedido en el repositorio")
                raise Exception("Error interno al guardar el pedido")

        except Exception as e:
            logger.exception(f"Error al crear el pedido: {str(e)}")
            raise e

    def listar_pedidos(self) -> List[PedidoModel]:
        try:
            pedidos = self.repo.listar_pedidos()
            if pedidos:
                logger.info(f"Se listaron {len(pedidos)} pedidos correctamente")
                return pedidos
            else:
                logger.info("No se encontraron pedidos")
                return []
        except Exception as e:
            logger.exception(f"Error al listar pedidos: {str(e)}")
            raise e


    def listar_pedidos_del_cliente(self, cliente_id: int) -> List[PedidoModel]:
        try:
            if not cliente_id:
                logger.warning("Cliente_id no proporcionado para listar pedidos")
                raise ValueError("cliente_id es obligatorio")
            pedidos = self.repo.listar_pedidos_del_cliente(cliente_id)
            if pedidos:
                logger.info(f"Se listaron {len(pedidos)} pedidos del cliente {cliente_id}")
                return pedidos
            else:
                logger.info(f"No se encontraron pedidos para el cliente {cliente_id}")
                return []
        except Exception as e:
            logger.exception(f"Error al listar pedidos del cliente: {str(e)}")
            raise e

    def eliminar_pedido_por_id(self, id: int) -> bool:
        try:
            if not id:
                logger.warning("ID no proporcionado para eliminar pedido")
                raise ValueError("El ID del pedido es obligatorio")
            eliminado = self.repo.eliminar_pedido_por_id(id)
            if eliminado:
                logger.info(f"Pedido con ID {id} eliminado correctamente")
                return True
            else:
                logger.info(f"No se encontró el pedido con ID {id} para eliminar")
                return False
        except Exception as e:
            logger.exception(f"Error al eliminar pedido: {str(e)}")
            raise e

    def actualizar_pedido_por_id(self, id: int, datos_actualizados: dict) -> bool:
        try:
            if not id:
                logger.warning("ID no proporcionado para actualizar pedido")
                raise ValueError("El ID del pedido es obligatorio")
            if not datos_actualizados:
                logger.warning("Datos vacíos para actualizar pedido")
                raise ValueError("Debe proporcionar datos a actualizar")
            actualizado = self.repo.actualizar_pedido_por_id(id, datos_actualizados)
            if actualizado:
                logger.info(f"Pedido con ID {id} actualizado correctamente")
                return True
            else:
                logger.info(f"No se encontró el pedido con ID {id} para actualizar")
                return False
        except Exception as e:
            logger.exception(f"Error al actualizar pedido: {str(e)}")
            raise e

   