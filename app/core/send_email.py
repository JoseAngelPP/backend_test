import requests
from django.conf import settings


def send_simple_message(subject, message, recipients):
    return requests.post(
        settings.MAILGUN_API_URL,
        auth=("api", settings.MAILGUN_PRIVATE_API_KEY),
        data={
            "from": settings.MAILGUN_HOST_USER,
            "to": recipients,
            "subject": subject,
            "text": message,
        },
    )
