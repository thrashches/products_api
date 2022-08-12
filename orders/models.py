from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator


User = get_user_model()


STATE_CHOICES = (
    ('basket', 'В корзине'),
    ('new', 'Новый'),
    ('confirmed', 'Подтвержден'),
    ('assembled', 'Собран'),
    ('sent', 'Отправлен'),
    ('delivered', 'Доставлен'),
    ('canceled', 'Отменен'),
)


class Order(models.Model):
    """Модель заказа"""
    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    user = models.ForeignKey(
        User, verbose_name='пользователь', on_delete=models.CASCADE)
    date_time = models.DateTimeField(
        verbose_name='время размещения заказа', auto_now_add=True)
    status = models.CharField(
        max_length=9,
        default='basket',
        choices=STATE_CHOICES,
        verbose_name='статус заказа')
    contact = models.ForeignKey('customers.Contact', blank=True, null=True,
                                on_delete=models.CASCADE, verbose_name='контакт клиента')

    def __str__(self):
        return f'{self.id} | {self.user.email} | {self.date_time}'


class OrderItem(models.Model):
    """Модель позиции заказа"""
    class Meta:
        verbose_name = 'Позиция заказа'
        verbose_name_plural = 'Позиции заказов'
        unique_together = [
            'order',
            'product_info',
        ]

    order = models.ForeignKey(
        Order, verbose_name='заказ', related_name='order_items', on_delete=models.CASCADE)
    product_info = models.ForeignKey(
        'goods.ProductInfo', verbose_name='товар', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, validators=[
        MinValueValidator(1),
    ], verbose_name='количество')

    def __str__(self):
        return f'{self.order.id}: {self.product_info.name}'
