from app.drive_config import drive_service
from app.Service.IDriveService import IDriveService
from app.Model.DriveModel import DriveModel
import logging
logger = logging.getLogger(__name__)

class DriveService(IDriveService):
    """
    Servicio para gestionar carpetas en Google Drive.
    """

    def crear_carpeta(self, nombre: str, parent_id: str) -> str:
        """
        Crea una carpeta en Google Drive dentro de parent_id.
        """
        file_metadata = {
            'name': nombre,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [parent_id]
        }
        file = drive_service.files().create(body=file_metadata, fields='id').execute()
        return file.get('id')

    def buscar_carpeta(self, nombre: str, parent_id: str) -> str | None:
        """
        Busca si existe una carpeta con el nombre dado dentro de parent_id.
        """
        query = (
            f"mimeType='application/vnd.google-apps.folder' "
            f"and trashed=false "
            f"and name='{nombre}' "
            f"and '{parent_id}' in parents"
        )
        response = drive_service.files().list(q=query, fields='files(id, name)').execute()
        files = response.get('files', [])
        if files:
            return files[0]['id']
        return None

    def buscar_o_crear_carpeta(self, nombre: str, parent_id: str) -> str:
        """
        Busca una carpeta; si no existe, la crea.
        """
        carpeta_id = self.buscar_carpeta(nombre, parent_id)
        if carpeta_id:
            return carpeta_id
        return self.crear_carpeta(nombre, parent_id)

    def crear_jerarquia_de_carpetas(self, drive: DriveModel) -> dict:
        """
        Crea la jerarquía:
        Cliente / Documentación / Año / Mes / Número de contrato.
        Devuelve los IDs de cada carpeta y un resumen de qué carpetas ya existían.
        """
        try:
            # Validaciones previas (puedes dejar o quitar si ya usas Pydantic)
            if not drive.cliente:
                logger.warning("Falta especificar el nombre del cliente")
                raise ValueError("El cliente no puede ser nulo")
            if not drive.carpeta_raiz_id:
                logger.warning("Falta especificar el id de la carpeta raíz")
                raise ValueError("El id de la carpeta raíz no puede ser nulo")
            if not drive.year:
                logger.warning("Falta especificar el año")
                raise ValueError("El año no puede ser nulo")
            if not drive.mes:
                logger.warning("Falta especificar el mes")
                raise ValueError("El mes no puede ser nulo")
            if not drive.numero_contrato:
                logger.warning("Falta especificar el número de contrato")
                raise ValueError("El número de contrato no puede ser nulo")

            # Lista de carpetas a crear (nombre, parent_id)
            carpetas = [
                ('cliente', drive.cliente, drive.carpeta_raiz_id),
                ('documentacion', 'Documentación', None),  # parent se asignará luego
                ('year', str(drive.year), None),
                ('mes', str(drive.mes), None),
                ('contrato', drive.numero_contrato, None),
                ("soportes de pago", "Soportes de Pago", None)

            ]

            resultados = {}
            resumen = {}

            # Creamos cliente primero
            cliente_id_existente = self.buscar_carpeta(drive.cliente, drive.carpeta_raiz_id)
            if cliente_id_existente:
                resultados['cliente_id'] = cliente_id_existente
                resumen['cliente'] = "ya existía"
            else:
                cliente_id = self.crear_carpeta(drive.cliente, drive.carpeta_raiz_id)
                resultados['cliente_id'] = cliente_id
                resumen['cliente'] = "creada"

            # Documentación dentro de cliente
            documentacion_id_existente = self.buscar_carpeta('Documentación', resultados['cliente_id'])
            if documentacion_id_existente:
                resultados['documentacion_id'] = documentacion_id_existente
                resumen['documentacion'] = "ya existía"
            else:
                documentacion_id = self.crear_carpeta('Documentación', resultados['cliente_id'])
                resultados['documentacion_id'] = documentacion_id
                resumen['documentacion'] = "creada"

            # Año dentro de cliente (ojo: dentro de cliente, no dentro de Documentación)
            year_id_existente = self.buscar_carpeta(str(drive.year), resultados['cliente_id'])
            if year_id_existente:
                resultados['year_id'] = year_id_existente
                resumen['year'] = "ya existía"
            else:
                year_id = self.crear_carpeta(str(drive.year), resultados['cliente_id'])
                resultados['year_id'] = year_id
                resumen['year'] = "creada"

            # Mes dentro de año
            mes_id_existente = self.buscar_carpeta(str(drive.mes), resultados['year_id'])
            if mes_id_existente:
                resultados['mes_id'] = mes_id_existente
                resumen['mes'] = "ya existía"
            else:
                mes_id = self.crear_carpeta(str(drive.mes), resultados['year_id'])
                resultados['mes_id'] = mes_id
                resumen['mes'] = "creada"

            # Contrato dentro de mes
            contrato_id_existente = self.buscar_carpeta(drive.numero_contrato, resultados['mes_id'])
            if contrato_id_existente:
                resultados['contrato_id'] = contrato_id_existente
                resumen['contrato'] = "ya existía"
            else:
                contrato_id = self.crear_carpeta(drive.numero_contrato, resultados['mes_id'])
                resultados['contrato_id'] = contrato_id
                resumen['contrato'] = "creada"

             # Soporte de Pago dentro del numero de contrato
            soporte_id_existente = self.buscar_carpeta('Soportes de Pago', resultados['contrato_id'])
            if soporte_id_existente:
                resultados['soporte_id'] = soporte_id_existente
                resumen['documentacion'] = "ya existía"
            else:
                soporte_id = self.crear_carpeta('Soportes de Pago', resultados['contrato_id'])
                resultados['soporte_id'] = soporte_id
                resumen['soportes de pago'] = "creada"

            logger.info(f"Resumen de creación de carpetas: {resumen}")

            return {
                "ids": resultados,
                "resumen": resumen
            }

        except Exception as e:
            logger.exception(f"Error al crear la jerarquía de carpetas: {str(e)}")
            raise e
