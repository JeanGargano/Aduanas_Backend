#Archivo de configuración para la conexión con mysql y Twilio
from pydantic_settings import BaseSettings
import mysql.connector


class Settings(BaseSettings):
    MYSQL_HOST: str
    MYSQL_USER: str
    MYSQL_PASSWORD: str
    MYSQL_DATABASE: str
    twilio_account_sid: str
    twilio_auth_token: str
    twilio_phone_number: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"

    class Config:
        env_file = ".env"

settings = Settings()
print("MYSQL_HOST:", Settings().MYSQL_HOST)


connection = mysql.connector.connect(
    host=settings.MYSQL_HOST,
    user=settings.MYSQL_USER,
    password=settings.MYSQL_PASSWORD,
    database=settings.MYSQL_DATABASE
)

if connection.is_connected():
    print("Connected to MySQL database")
