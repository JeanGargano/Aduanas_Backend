import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from fastapi import HTTPException
from app.Model.EmailModel import EmailModel
from app.Service.IEmailService import IEmailService
from app.configurations import settings

# Configuración del logger
logger = logging.getLogger(__name__)

# Configuración del remitente
REMITENTE = settings.REMITENTE
CONTRASENA = settings.CONTRASENA
SMTP_SERVER = settings.SMTP_SERVER
SMTP_PORT = settings.SMTP_PORT

class EmailService(IEmailService):

    def enviar_correo(self, data: EmailModel) -> str:
        if not data.destinatario:
            raise HTTPException(status_code=422, detail="El campo 'destinatario' es obligatorio.")
        if not data.asunto.strip():
            raise HTTPException(status_code=422, detail="El campo 'asunto' no puede estar vacío.")

        try:
            msg = MIMEMultipart()
            msg["From"] = REMITENTE
            msg["To"] = data.destinatario
            msg["Subject"] = data.asunto

            mensaje = f"""
                Buenas tardes, Confirmo entrega:

                - Pedido: {data.numero_contrato}
                - Producto: {data.producto}
                - Contenedor: {data.contender}
                - Días Libres: {data.dias_libres}
                - Puerto: {data.puerto}
                """
            msg.attach(MIMEText(mensaje, "plain"))

            # Conexión al servidor SMTP
            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=30) as server:
                server.starttls()  # Cifrar la conexión
                server.login(REMITENTE, CONTRASENA)
                server.sendmail(REMITENTE, data.destinatario, msg.as_string())

            logger.info(f"Correo enviado correctamente a {data.destinatario}")
            return {"status": "ok", "message": "Correo enviado con éxito 🚀"}

        except smtplib.SMTPAuthenticationError:
            logger.error("Error de autenticación SMTP (verifica usuario/contraseña).")
            raise HTTPException(status_code=401, detail="Error de autenticación con el servidor de correo.")
        except smtplib.SMTPConnectError:
            logger.error("No se pudo conectar al servidor SMTP.")
            raise HTTPException(status_code=503, detail="No se pudo conectar al servidor de correo.")
        except smtplib.SMTPException as e:
            logger.error(f"Error SMTP: {e}")
            raise HTTPException(status_code=500, detail="Error en el envío de correo.")
        except Exception as e:
            logger.exception("Error inesperado en EmailService")
            raise HTTPException(status_code=500, detail="Error inesperado en el servicio de correo.")
