#Archivo de configuracion para la conexion con el servicio de drive
from google.oauth2 import service_account
from googleapiclient.discovery import build

SERVICE_ACCOUNT_FILE = 'aduanas-backend-28de18b87eee.json'
SCOPES = ['https://www.googleapis.com/auth/drive']

# Crear credenciales
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)

# Crear cliente de Drive
drive_service = build('drive', 'v3', credentials=credentials)
