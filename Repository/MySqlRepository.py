#Metodos de inicializacón
from configurations import settings
import mysql.connector

class MySqlRepository:
    
    def get_connection(self):
        return mysql.connector.connect(
            host=settings.MYSQL_HOST,
            user=settings.MYSQL_USER,
            password=settings.MYSQL_PASSWORD,
            database=settings.MYSQL_DATABASE
        )
