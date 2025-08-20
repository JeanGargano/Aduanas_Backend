from app.Model.EmailModel import EmailModel
from abc import abstractmethod, ABC

class IEmailService(ABC):
    @abstractmethod
    def enviarCorreo(self, data: EmailModel) -> str:
        pass

