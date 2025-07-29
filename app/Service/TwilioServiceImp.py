from app.Service.ITwilioService import ITwilioService
from app.Repository.TwilioRepository import TwilioRepository
from app.Model.TwilioModel import TwilioModel
from fastapi import Depends
import logging


logger = logging.getLogger(__name__)

class TwilioServiceImp(ITwilioService):
    def __init__(self, repo: TwilioRepository = Depends()):
        self.repo = repo

    def enviar_mensaje(self, twilio: TwilioModel) -> str:
        try:
            if not twilio:
                logger.warning("Objeto vacio o nulo")
                raise ValueError("El objeto no puede ser nulo")

            if not twilio.numero:
                logger.warning("Objeto inválido: falta el numero del cliente")
                raise ValueError("El numero del cliente es obligatorio para crear el pedido")
            if not twilio.mensaje:
                logger.warning("Objeto invalido: falta el mensaje")
                raise ValueError("El mensaje debe ser obligatorio")
            numero = twilio.numero
            mensaje = twilio.mensaje
            res = self.repo.enviar_mensaje(numero, mensaje)
            if res:
                logger.info(f"Mensaje enviado exitosamente: {res}")
                return f"Mensaje enviado al numero: {twilio.numero}"
            else:
                logger.error("No se pudo enviar el mensaje")
                raise Exception("Error interno al enviar el mensaje")

        except Exception as e:
            logger.exception(f"Error al enviar el mensaje: {str(e)}")
            raise e