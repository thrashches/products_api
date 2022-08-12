from django.core.mail import send_mail
from django.conf import settings


def send_email(user):
    send_mail(
        'Информация о вашем заказе',
        'Ваш заказ был успешно оформлен!',
        settings.DEFAULT_FROM_EMAIL,
        [user.email]
    )
