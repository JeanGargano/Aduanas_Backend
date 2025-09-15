# Archivo de configuración para la conexión con mysql y Twilio
from pydantic_settings import BaseSettings
import mysql.connector
from typing import Optional


class Settings(BaseSettings):
    # Variables para Base de datos
    MYSQL_HOST: str
    MYSQL_USER: str
    MYSQL_PASSWORD: str
    MYSQL_DATABASE: str
    MYSQL_PORT: int 

    # Variables para Twilio
    TWILIO_ACCOUNT_SID: str
    TWILIO_AUTH_TOKEN: str
    TWILIO_PHONE_NUMBER: str

    # Variables para Sengrid
    SENDGRID_API_KEY: str
    SENDGRID_FROM_EMAIL: str

    # Variables para seguridad
    SECRET_KEY: str
    ALGORITHM: str 
    
    # Google Drive Service Account variables
    GOOGLE_TYPE: Optional[str] = "service_account"
    GOOGLE_PROJECT_ID: Optional[str] = None
    GOOGLE_PRIVATE_KEY_ID: Optional[str] = None
    GOOGLE_PRIVATE_KEY: Optional[str] = None
    GOOGLE_CLIENT_EMAIL: Optional[str] = None
    GOOGLE_CLIENT_ID: Optional[str] = None
    GOOGLE_AUTH_URI: Optional[str] = "https://accounts.google.com/o/oauth2/auth"
    GOOGLE_TOKEN_URI: Optional[str] = "https://oauth2.googleapis.com/token"
    GOOGLE_AUTH_PROVIDER_CERT_URL: Optional[str] = "https://www.googleapis.com/oauth2/v1/certs"
    GOOGLE_CLIENT_CERT_URL: Optional[str] = None
    GOOGLE_UNIVERSE_DOMAIN: Optional[str] = "googleapis.com"


    class Config:
        env_file = ".env"
        extra = "ignore"

# Instancia única
settings = Settings()

# Conexión a MySQL con manejo de errores
try:
    connection = mysql.connector.connect(
        host=settings.MYSQL_HOST,
        user=settings.MYSQL_USER,
        password=settings.MYSQL_PASSWORD,
        database=settings.MYSQL_DATABASE,
        port=settings.MYSQL_PORT
    )
    
    if connection.is_connected():
        print("Connected to MySQL database")
        
except mysql.connector.Error as e:
    print(f"Error connecting to MySQL: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")