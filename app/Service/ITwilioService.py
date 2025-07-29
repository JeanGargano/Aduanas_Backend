from app.Model.TwilioModel import TwilioModel
from abc import abstractmethod, ABC

class ITwilioService(ABC):

    @abstractmethod
    def enviar_mensaje(self, twilio: TwilioModel) -> str:
        pass
