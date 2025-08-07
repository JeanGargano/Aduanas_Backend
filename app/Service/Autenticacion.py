from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from app.configurations import Settings
from app.Service.UsuarioServiceImp import UsuarioServiceImp
from fastapi import Depends as FastapiDepends

cfg = Settings()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

def verificar_token(token: str):
    try:
        payload = jwt.decode(token, cfg.SECRET_KEY, algorithms=[cfg.ALGORITHM])
        sub = payload.get("sub")
        if sub is None:
            raise JWTError("subject not found")
        return payload
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )

def get_current_user(token: str = Depends(oauth2_scheme), service: UsuarioServiceImp = FastapiDepends()):   
    verificar_token(token)
    payload = jwt.decode(token, cfg.SECRET_KEY, algorithms=[cfg.ALGORITHM])
    identificacion = int(payload.get("sub"))
    usuario = service.repo.buscar_usuario(identificacion)
    if not usuario:
        raise HTTPException(status_code=401, detail="Usuario no existe")
    return usuario
