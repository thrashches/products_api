import string
import random
from django.core.mail import send_mail
from django.conf import settings


def generate_token():
    """Генерирует строку из 64 случайных символов"""
    return ''.join(random.choice(string.ascii_letters) for i in range(64))


def send_email(email, subject, message):
    """Отправляет письмо пользователю"""
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [email]
    )
