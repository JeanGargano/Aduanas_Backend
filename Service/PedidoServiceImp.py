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

            if not pedido.id_cliente:
                logger.warning("Pedido inválido: falta id_cliente")
                raise ValueError("id_cliente es obligatorio para crear el pedido")

            creado = self.repo.crear_pedido(pedido)
            if creado:
                logger.info(f"Pedido creado correctamente")
                return f"Pedido creado exitosamente"
            else:
                logger.error("No se pudo crear el pedido")
                raise Exception("Error interno al guardar el pedido")

        except Exception as e:
            logger.exception(f"Error al crear el pedido: {str(e)}")
            raise e

    def listar_pedidos(self) -> List[PedidoModel]:
        try:
            pedidos = self.repo.listar_pedidos()
            if pedidos:
                logger.info(f"Se listaron {len(pedidos)} pedidos correctamente")
                #print(pedidos)
                return pedidos
            else:
                logger.info("No se encontraron pedidos")
                return []
        except Exception as e:
            logger.exception(f"Error al listar pedidos: {str(e)}")
            raise e


    def listar_pedidos_del_cliente(self, id_cliente: int) -> List[PedidoModel]:
        try:
            if not id_cliente:
                logger.warning("Identificacion del cliente no proporcionada para listar los pedidos")
                raise ValueError("La identificación es obligatoria")
            pedidos = self.repo.listar_pedidos_del_cliente(id_cliente)
            if pedidos:
                logger.info(f"Se listaron {len(pedidos)} pedidos del cliente {id_cliente}")
                return pedidos
            else:
                logger.info(f"No se encontraron pedidos para el cliente {id_cliente}")
                return []
        except Exception as e:
            logger.exception(f"Error al listar pedidos del cliente: {str(e)}")
            raise e
        
        
    def listar_pedido_por_id(self, id_pedido: int) -> List[PedidoModel]:
        try:
            if not id_pedido:
                logger.warning("Id del pedido no proporcionado para poder listarlo")
                raise ValueError("El id es obligatorio")
            pedido = self.repo.listar_pedido_por_id(id_pedido)
            if pedido:
                logger.info(f"Se listo el pedido")
                return pedido
            else:
                logger.info(f"No se encontraron pedidos para el id:  {id_pedido}")
                return []
        except Exception as e:
            logger.exception(f"Error al listar el pedido: {str(e)}")
            raise e
        

    def actualizar_pedido_por_id(self, id_pedido: int, datos_actualizados: dict) -> bool:
        try:
            if not id_pedido:
                logger.warning("ID no proporcionado para actualizar pedido")
                raise ValueError("El ID del pedido es obligatorio")
            if not datos_actualizados:
                logger.warning("Datos vacíos para actualizar pedido")
                raise ValueError("Debe proporcionar datos a actualizar")
            actualizado = self.repo.actualizar_pedido_por_id(id_pedido, datos_actualizados)
            if actualizado:
                logger.info(f"Pedido con ID {id_pedido} actualizado correctamente")
                return True
            else:
                logger.info(f"No se encontró el pedido con ID {id_pedido} para actualizar")
                return False
        except Exception as e:
            logger.exception(f"Error al actualizar pedido: {str(e)}")
            raise e

        



   