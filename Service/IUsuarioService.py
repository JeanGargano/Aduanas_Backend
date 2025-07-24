#Clase abstracta donde van definidos los metodos para formulario
from abc import abstractmethod, ABC
from Model.UsuarioModel import UsuarioModel
from typing import List, Optional

class IUsuarioService(ABC):

    #Metodo abstracto para crear Cliente
    @abstractmethod
    def crear_usuario(self, cliente:UsuarioModel) -> str:
        pass

    #Metodo abtracto para listar clientes
    @abstractmethod
    def listar_usuarios(self) ->List[UsuarioModel]:
        pass
    
    #Metodo abstracto para listar clientes por id
    @abstractmethod
    def listar_usuario_por_id(self, identificacion: int) -> List[UsuarioModel]:
        pass

    #Metodo abstracto para actualizar cliente por id
    @abstractmethod
    def actualizar_usuario_por_id(self, identificacion: int, datos_actualizados: dict) -> bool:
        pass

    #Metodo abstracto para asignar contraseña
    @abstractmethod
    def asignar_contraseña(self, identificacion: int, contraseña: str) -> str:
        pass
    

    #Metodo Abstracto para logear auditor externo
    @abstractmethod
    def logear_usuario(self, identificacion: str, contraseña: str) -> Optional[UsuarioModel]:
        pass


   


