from rest_framework.decorators import action
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from customers.permissions import IsProvider
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from .models import Shop, Category, Product, ProductInfo, Parameter, ProductParameter
from .serializers import ProductInfoSerializer, GoodsUploadSerializer
from drf_spectacular.utils import extend_schema, OpenApiParameter
from yaml import load
from yaml.parser import ParserError
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader


class ProductInfoViewset(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                         viewsets.GenericViewSet
                         ):
    """Вьюсет для работы с товарами"""
    queryset = ProductInfo.objects.all()
    serializer_class = ProductInfoSerializer

    def list(self, request, *args, **kwargs):
        """Отображение списка товаров"""
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """Отображение карточки товара"""
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        request=GoodsUploadSerializer
    )
    @action(detail=False, methods=['post'], permission_classes=[IsProvider])
    def upload(self, request):
        """Загрузка товаров из yml-файла"""
        try:
            url = request.data['url']
            validator = URLValidator()
            validator(url)
            data = load(request.FILES['data'], Loader)

            shop, created = Shop.objects.get_or_create(name=data['shop'])
            shop.url = url
            shop.save()

            for category_data in data['categories']:
                category, created = Category.objects.get_or_create(
                    id=category_data['id'])
                category.name = category_data['name']
                category.save()

            ProductInfo.objects.filter(shop=shop).delete()
            for item in data['goods']:
                product, created = Product.objects.get_or_create(
                    name=item['name'], category_id=item['category'])
                product_info = ProductInfo.objects.create(
                    article_number=item['id'],
                    product_id=product.id,
                    shop_id=shop.id,
                    model=item['model'],
                    name=item['name'],
                    quantity=item['quantity'],
                    price=item['price'],
                    price_rrc=item['price_rrc']
                )
                for param_name, param_value in item['parameters'].items():
                    param, created = Parameter.objects.get_or_create(
                        name=param_name)
                    ProductParameter.objects.create(
                        product_info_id=product_info.id,
                        parameter_id=param.id,
                        value=param_value
                    )

            return Response(data={'status': f'Успешно загружено {len(data["goods"])}!'}, status=HTTP_201_CREATED)
        except ParserError:
            return Response(data={'error': 'Неверный формат yaml файла!'}, status=HTTP_400_BAD_REQUEST)
        except ValidationError:
            return Response(data={'error': 'Неверный url магазина!'}, status=HTTP_400_BAD_REQUEST)
