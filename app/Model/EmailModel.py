from pydantic import BaseModel, EmailStr

class EmailModel(BaseModel):
    destinatario: EmailStr
    asunto: str
    numero_contrato: str
    producto: str
    contender: str
    puerto: str
    dias_libres: str

