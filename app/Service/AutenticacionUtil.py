from datetime import datetime, timedelta
from jose import jwt
from dotenv import load_dotenv
from app.configurations import settings
import os

load_dotenv()

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM

def crear_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=30)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
