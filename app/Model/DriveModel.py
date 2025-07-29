from pydantic import BaseModel

class DriveModel(BaseModel):
    cliente: str
    numero_contrato: str
    year: int
    mes: int
    carpeta_raiz_id: str