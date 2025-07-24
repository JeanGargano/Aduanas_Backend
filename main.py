#Flujo principal
from fastapi import FastAPI, APIRouter, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import uvicorn
from dotenv import load_dotenv 
from Controller.PedidoController import router as pedido_router
from Controller.DriveController import router as drive_router
from Controller.TwilioController import router as twilio_router
from Controller.UsuarioController import router as usuario_router
import logging

logger = logging.getLogger(__name__)

import logging
import os

#Configuracion de logs
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


#Cargar variables de entorno desde el archivo .env
load_dotenv()

#Inicializar la aplicación FastAPI
app = FastAPI()

api_router = APIRouter()

# Incluir los controladores en la API
api_router.include_router(pedido_router, prefix="/pedido", tags=["Pedido"])
api_router.include_router(drive_router, prefix="/drive", tags=["Drive"])
api_router.include_router(twilio_router, prefix="/twilio", tags=["Twilio"])
api_router.include_router(usuario_router, prefix="/usuario", tags=["Usuario"])
# Incluir el router principal
app.include_router(api_router)
    
# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ejecutar la aplicación
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)



