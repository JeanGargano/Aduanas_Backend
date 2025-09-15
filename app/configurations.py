#Archivo de configuración para la conexión con mysql y Twilio
from pydantic_settings import BaseSettings
import mysql.connector
from typing import Optional


class IgnoredType:
    pass


class Settings(BaseSettings):
    MYSQL_HOST: str
    MYSQL_USER: str
    MYSQL_PASSWORD: str
    MYSQL_DATABASE: str
    MYSQL_PORT: int = IgnoredType()
    twilio_account_sid: str
    twilio_auth_token: str
    twilio_phone_number: str
    SECRET_KEY: str
    ALGORITHM: str 
    REMITENTE: str
    CONTRASENA: str
    SMTP_SERVER: str
    SMTP_PORT: int = IgnoredType()
    
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

settings = Settings()
print("MYSQL_HOST:", Settings().MYSQL_HOST)


connection = mysql.connector.connect(
    host=settings.MYSQL_HOST,
    user=settings.MYSQL_USER,
    password=settings.MYSQL_PASSWORD,
    database=settings.MYSQL_DATABASE,
    port=settings.MYSQL_PORT
)

if connection.is_connected():
    print("Connected to MySQL database")