from Model.DriveModel import DriveModel
from abc import abstractmethod, ABC

class IDriveService(ABC):

    @abstractmethod
    def crear_carpeta(self, nombre: str, parent_id: int) -> str:
        pass

    @abstractmethod
    def buscar_carpeta(self, nombre: str, parent_id:str) -> str:
        pass

    @abstractmethod
    def buscar_o_crear_carpeta(self, nombre: str, parent_id: str) -> str:
        pass

    @abstractmethod
    def crear_jerarquia_de_carpetas(self, drive: DriveModel) -> str:
        pass
