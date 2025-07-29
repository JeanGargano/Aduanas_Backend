from abc import abstractmethod, ABC
from app.Model.PedidoModel import PedidoModel
from typing import List

class IPedidoService(ABC):

    
    @abstractmethod
    def crear_pedido(self, pedido:PedidoModel) -> str:
        pass

    
    @abstractmethod
    def listar_pedidos(self) ->List[PedidoModel]:
        pass

    
    @abstractmethod
    def listar_pedidos_del_cliente(self, id_cliente: int) -> List[PedidoModel]:
        pass

    @abstractmethod
    def listar_pedido_por_id(self, id_pedido: int) -> List[PedidoModel]:
        pass

    
    @abstractmethod
    def actualizar_pedido_por_id(self, id_pedido: int, datos_actualizados: dict) -> bool:
        pass

   


