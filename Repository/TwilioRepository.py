from twilio.rest import Client
from configurations import settings 

class TwilioRepository:
    def __init__(self):
        self.account_sid = settings.twilio_account_sid
        self.auth_token = settings.twilio_auth_token
        self.whatsapp_from = settings.twilio_phone_number 
        self.client = Client(self.account_sid, self.auth_token)

    def enviar_mensaje(self, numero: str, mensaje: str) -> str:
        numero_formateado = f"whatsapp:{numero}"
        message = self.client.messages.create(
            body=mensaje,
            from_=self.whatsapp_from,
            to=numero_formateado
        )
        return message.sid
