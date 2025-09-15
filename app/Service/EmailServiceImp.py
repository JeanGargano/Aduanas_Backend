import logging
from fastapi import HTTPException
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from app.Model.EmailModel import EmailModel
from app.Service.IEmailService import IEmailService
from app.configurations import settings

# Configuración del logger
logger = logging.getLogger(__name__)

class EmailService(IEmailService):

    def enviarCorreo(self, data: EmailModel) -> str:
        if not data.destinatario:
            raise HTTPException(status_code=422, detail="El campo 'destinatario' es obligatorio.")
        if not data.asunto.strip():
            raise HTTPException(status_code=422, detail="El campo 'asunto' no puede estar vacío.")

        try:
            # Definir el contenido del correo
            estado = data.estado
            if estado == "ENTREGADO":
                contenido = f"""
                Buenas tardes, Confirmo entrega:

                - Pedido: {data.numero_contrato}
                - Producto: {data.producto}
                - Contenedor: {data.contenedor}
                - Días Libres: {data.dias_libres}
                - Puerto: {data.puerto}
                """
            else:
                contenido = f"""
                Hola apreciado cliente, el estado de su pedido ha sido actualizado a {estado}:
                - Pedido: {data.numero_contrato}
                - Producto: {data.producto}
                - Contenedor: {data.contenedor}
                - Días Libres: {data.dias_libres}
                - Puerto: {data.puerto}
                """

            # Crear mensaje con SendGrid
            message = Mail(
                from_email=settings.SENDGRID_FROM_EMAIL,
                to_emails=data.destinatario,
                subject=data.asunto,
                plain_text_content=contenido
            )

            # Cliente SendGrid
            sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
            response = sg.send(message)

            if response.status_code in [200, 202]:
                logger.info(f"Correo enviado correctamente a {data.destinatario}")
                return {"status": "ok", "message": "Correo enviado con éxito 🚀"}
            else:
                logger.error(f"Error al enviar correo. Status: {response.status_code}, Body: {response.body}")
                raise HTTPException(status_code=500, detail="Error en el envío de correo.")

        except Exception as e:
            logger.exception("Error inesperado en EmailService con SendGrid")
            raise HTTPException(status_code=500, detail=f"Error inesperado en el servicio de correo: {e}")
