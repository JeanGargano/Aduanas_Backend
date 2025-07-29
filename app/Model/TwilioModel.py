from pydantic import BaseModel

class TwilioModel(BaseModel):
    numero: str
    mensaje: str