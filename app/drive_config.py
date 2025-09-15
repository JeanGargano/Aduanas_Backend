# Archivo de configuracion para la conexion con el servicio de drive
import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from app.configurations import settings  # Importar settings de Pydantic

SCOPES = ['https://www.googleapis.com/auth/drive']

def get_drive_service():
    """
    Obtiene el servicio de Google Drive usando credenciales de la clase Settings
    """
    try:
        # Verificar que las variables existan usando Pydantic settings
        if not all([settings.GOOGLE_PROJECT_ID, settings.GOOGLE_PRIVATE_KEY, settings.GOOGLE_CLIENT_EMAIL]):
            raise ValueError("Faltan credenciales de Google en la configuración")
        
        # Construir el diccionario de credenciales desde Pydantic Settings
        service_account_info = {
            "type": settings.GOOGLE_TYPE,
            "project_id": settings.GOOGLE_PROJECT_ID,
            "private_key_id": settings.GOOGLE_PRIVATE_KEY_ID,
            "private_key": settings.GOOGLE_PRIVATE_KEY.replace("\\n", "\n"),
            "client_email": settings.GOOGLE_CLIENT_EMAIL,
            "client_id": settings.GOOGLE_CLIENT_ID,
            "auth_uri": settings.GOOGLE_AUTH_URI,
            "token_uri": settings.GOOGLE_TOKEN_URI,
            "auth_provider_x509_cert_url": settings.GOOGLE_AUTH_PROVIDER_CERT_URL,
            "client_x509_cert_url": settings.GOOGLE_CLIENT_CERT_URL,
            "universe_domain": settings.GOOGLE_UNIVERSE_DOMAIN
        }

        
        # Debug info (puedes quitar esto después)
        print(f"🔧 Project ID: {service_account_info['project_id']}")
        print(f"🔧 Client Email: {service_account_info['client_email']}")
        print(f"🔧 Private Key Length: {len(service_account_info['private_key']) if service_account_info['private_key'] else 0}")
        
        # Crear credenciales desde el diccionario
        credentials = service_account.Credentials.from_service_account_info(
            service_account_info, scopes=SCOPES
        )
        
        # Crear cliente de Drive
        drive_service = build('drive', 'v3', credentials=credentials)
        print("✅ Servicio de Google Drive configurado correctamente")
        return drive_service
        
    except Exception as e:
        print(f"❌ Error al configurar el servicio de Google Drive: {e}")
        raise e

# Crear instancia del servicio
drive_service = get_drive_service()