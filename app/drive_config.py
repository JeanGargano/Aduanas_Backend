# Archivo de configuracion para la conexion con el servicio de drive
import os
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/drive']

def get_drive_service():
    """
    Obtiene el servicio de Google Drive usando credenciales de variables de entorno
    """
    try:
        # Intentar leer desde variable de entorno JSON
        service_account_json = os.environ.get('GOOGLE_SERVICE_ACCOUNT_JSON')
        
        if service_account_json:
            # Parsear el JSON desde la variable de entorno
            service_account_info = json.loads(service_account_json)
            
            # Crear credenciales desde el diccionario
            credentials = service_account.Credentials.from_service_account_info(
                service_account_info, scopes=SCOPES
            )
        else:
            raise ValueError("No se encontró GOOGLE_SERVICE_ACCOUNT_JSON en las variables de entorno")
        
        # Crear cliente de Drive
        drive_service = build('drive', 'v3', credentials=credentials)
        print("✅ Servicio de Google Drive configurado correctamente")
        return drive_service
        
    except Exception as e:
        print(f"❌ Error al configurar el servicio de Google Drive: {e}")
        raise e

# Crear instancia del servicio
drive_service = get_drive_service()