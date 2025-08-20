import sys
import os
from fastapi import Depends
from app.Service.Autenticacion import get_current_user

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from dotenv import load_dotenv 
from app.Controller.PedidoController import router as pedido_router
from app.Controller.DriveController import router as drive_router
from app.Controller.TwilioController import router as twilio_router
from app.Controller.UsuarioController import router as usuario_router
from app.Controller.NotificacionController import router as notificacion_router
from app.Controller.EmailController import router as email_router
import logging

logger = logging.getLogger(__name__)

import logging
import os

#Configuracion de logs
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


load_dotenv()

app = FastAPI()

api_router = APIRouter()

api_router.include_router(pedido_router, prefix="/pedido", tags=["Pedido"], dependencies=[Depends(get_current_user)])
api_router.include_router(drive_router, prefix="/drive", tags=["Drive"], dependencies=[Depends(get_current_user)])
api_router.include_router(twilio_router, prefix="/twilio", tags=["Twilio"], dependencies=[Depends(get_current_user)])
api_router.include_router(usuario_router, prefix="/usuario", tags=["Usuario"])
api_router.include_router(notificacion_router, prefix="/notificacion", tags=["Notificacion"], dependencies=[Depends(get_current_user)])
api_router.include_router(email_router, prefix="/smtp", tags=["SMTP"])

app.include_router(api_router)
    

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)



