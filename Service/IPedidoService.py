#Clase abstracta donde van definidos los metodos para formulario
from abc import abstractmethod, ABC
from Model.PedidoModel import PedidoModel
from typing import List, Optional

class IPedidoService(ABC):

    #Metodo abstracto para crear Pedido
    @abstractmethod
    def crear_pedido(self, pedido:PedidoModel) -> str:
        pass

    #Metodo abtracto para listar pedidos
    @abstractmethod
    def listar_pedidos(self) ->List[PedidoModel]:
        pass

    #Metodo abstracto para listar los pedidos de un cliente
    @abstractmethod
    def listar_pedidos_del_cliente(self, id_cliente: int) -> List[PedidoModel]:
        pass

    #Metodo abstracto para actualizar pedido por id
    @abstractmethod
    def actualizar_pedido_por_id(self, id_pedido: int) -> bool:
        pass

    #Metodo para actualizar el estado de un pedido
    @abstractmethod
    def actualizar_estado_pedido(self, id:int) -> bool:
        pass

   


