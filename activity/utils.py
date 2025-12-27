from django.core.mail import EmailMessage
from django.conf import settings


def setup_email(to_: str, subject: str, body: str) -> EmailMessage:
    return EmailMessage(
        subject=subject,
        body=body,
        to=[to_],
        from_email=settings.DEFAULT_FROM_EMAIL,
    )
