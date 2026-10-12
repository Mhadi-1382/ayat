
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

def send_mail(subject: str, body: str, html_context: str, to: list):
    try:
        message = EmailMultiAlternatives(
            subject=subject,
            body=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=to,
        )
        message.attach_alternative(html_context, 'text/html')
        message.send()
    except Exception as e:
        print(f'EMAIL_ERR: {e}')
