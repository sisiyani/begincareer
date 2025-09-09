from django.conf import settings
from azure.communication.email import EmailClient
from azure.core.exceptions import HttpResponseError

# Initialise le client ACS Email
sender = settings.ACS_EMAIL_SENDER
def get_email_client():
    return EmailClient.from_connection_string(settings.ACS_EMAIL_CONNECTION_STRING)
    
def send_acs_email(to_address, subject, plain_text, html_content=None):
    email_client = get_email_client()
    """Envoi d'email via Azure Communication Services"""
    message = {
        "senderAddress": sender,
        "recipients": {
            "to": [{"address": to_address}]
        },
        "content": {
            "subject": subject,
            "plainText": plain_text,
            "html": html_content or f"<p>{plain_text}</p>"
        }
    }

    try:
        poller = email_client.begin_send(message)
        result = poller.result()
        return result["id"]
    except HttpResponseError as ex:
        print("Erreur lors de l'envoi ACS Email:", ex)
        return None
