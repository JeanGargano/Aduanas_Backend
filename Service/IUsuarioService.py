from abc import abstractmethod, ABC
from Model.UsuarioModel import UsuarioModel
from typing import List

class IUsuarioService(ABC):

    
    @abstractmethod
    def crear_usuario(self, cliente:UsuarioModel) -> str:
        pass


    @abstractmethod
    def listar_usuarios(self) ->List[UsuarioModel]:
        pass
    
    
    @abstractmethod
    def listar_usuario_por_id(self, identificacion: int) -> List[UsuarioModel]:
        pass

    
    @abstractmethod
    def actualizar_usuario_por_id(self, identificacion: int, datos_actualizados: dict) -> bool:
        pass

    
    @abstractmethod
    def asignar_contraseña(self, identificacion: int, contraseña: str) -> bool:
        pass
    

    
    @abstractmethod
    def logear_usuario(self, identificacion: str, contraseña: str) -> UsuarioModel:
        pass


   


