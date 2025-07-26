from fastapi import APIRouter, HTTPException
from Service.DriveServiceImp import DriveService
from Model.DriveModel import DriveModel
from fastapi import Depends, Query, Body
router = APIRouter()


@router.post("/crear_carpetas_drive")
def crear_carpetas_drive(
    drive: DriveModel,
    service: DriveService = Depends()
):
    try:
        res = service.crear_jerarquia_de_carpetas(drive)
        resumen = res["resumen"]

        # Ver si al menos una fue creada
        if any(v == "creada" for v in resumen.values()):
            message = "Carpetas creadas exitosamente"
        else:
            message = "Todas las carpetas ya existían"

        return {"message": message, "informacion": res}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear carpetas en Drive: {str(e)}")
