from django.core.mail import send_mail
from django.conf import settings


def send_email(user, subject, message):
    """Отправляет письмо пользователю"""
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email]
    )
