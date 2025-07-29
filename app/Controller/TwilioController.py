from fastapi import APIRouter, Depends
from app.Service.TwilioServiceImp import TwilioServiceImp
from app.Model.TwilioModel import TwilioModel

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
