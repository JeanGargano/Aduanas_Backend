from app.configurations import settings
import mysql.connector
import logging

logger = logging.getLogger(__name__)

class MySqlRepository:
    def __init__(self):
        self.config = {
            "host": settings.MYSQL_HOST,
            "user": settings.MYSQL_USER,
            "password": settings.MYSQL_PASSWORD,
            "database": settings.MYSQL_DATABASE,
            "port": settings.MYSQL_PORT
        }

    def get_connection(self):
        return mysql.connector.connect(**self.config)
