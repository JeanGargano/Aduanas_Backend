from fastapi import APIRouter, Depends, HTTPException
from app.Model.EmailModel import EmailModel
from app.Service.EmailServiceImp import EmailService

router = APIRouter()

@router.post("/enviar_correo")
def enviar_correo(
    data: EmailModel,
    service: EmailService = Depends()
):
    try:
        return service.enviar_correo(data)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Ocurrió un error inesperado al enviar el correo."
        )
