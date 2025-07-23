#Controlador para manejar todas las solicitudes referentes al servicio de mensajeria
from fastapi import APIRouter, Depends
from Service.TwilioServiceImp import TwilioServiceImp
from Model.TwilioModel import TwilioModel

router = APIRouter()

@router.post("/enviar_mensaje")
def enviar_mensaje(
    twilio: TwilioModel,
    service: TwilioServiceImp = Depends()
):
    try:
        res = service.enviar_mensaje(twilio)
        return {"message": "Mensaje enviado", "sid": res}
    except Exception as e:
        return {"error": str(e)}
