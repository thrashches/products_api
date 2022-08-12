from django.db import models


class Shop(models.Model):
    """Модель магазина"""
    class Meta:
        verbose_name = 'Магазин'
        verbose_name_plural = 'Магазины'

    name = models.CharField(max_length=255, unique=True, verbose_name='название')
    url = models.URLField(verbose_name='сайт')

    def __str__(self) -> str:
        return self.name


class Category(models.Model):
    """Модель категории товара"""
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    shops = models.ManyToManyField(
        Shop,
        verbose_name='магазины, в которых представлена категория'
    )
    name = models.CharField(max_length=255, verbose_name='название')

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    """Модель товара"""
    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, verbose_name='категория')
    name = models.CharField(max_length=255, verbose_name='название')

    def __str__(self) -> str:
        return self.name


class ProductInfo(models.Model):
    """Модель информации о товаре"""
    class Meta:
        verbose_name = 'Информация о товаре'
        verbose_name_plural = 'Информация о товарах'
        unique_together = [
            'product',
            'shop',
        ]

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, verbose_name='товар')
    shop = models.ForeignKey(
        Shop, on_delete=models.CASCADE, verbose_name='магазин')
    article_number = models.IntegerField(verbose_name='артикул')
    model = models.CharField(max_length=255, verbose_name='модель')
    name = models.CharField(max_length=255, verbose_name='название')
    quantity = models.PositiveIntegerField(
        default=0, verbose_name='количество')
    price = models.DecimalField(
        max_digits=20, decimal_places=2, verbose_name='цена')
    price_rrc = models.DecimalField(
        max_digits=20, decimal_places=2, verbose_name='РРЦ')

    def __str__(self) -> str:
        return f'{self.shop.name} | {self.product.name} | {self.quantity} шт.'


class Parameter(models.Model):
    """Модель дополнительных свойств товара"""
    class Meta:
        verbose_name = 'Параметр'
        verbose_name_plural = 'Параметры'

    name = models.CharField(max_length=255, unique=True, verbose_name='название')

    def __str__(self) -> str:
        return self.name


class ProductParameter(models.Model):
    """Модель доп свойства товара с привязкой к товару"""
    class Meta:
        verbose_name = 'Параметр товара'
        verbose_name_plural = 'Параметры товаров'

    product_info = models.ForeignKey(
        ProductInfo, on_delete=models.CASCADE, related_name='product_parameters', verbose_name='информация о товаре')
    parameter = models.ForeignKey(
        Parameter, on_delete=models.CASCADE, verbose_name='параметр')
    value = models.CharField(max_length=255, verbose_name='значение')

    def __str__(self) -> str:
        return f'{self.parameter.name}: {self.value}'
