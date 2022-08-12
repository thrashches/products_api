from unicodedata import name
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from customers.permissions import IsProvider
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from .models import Shop, Category, Product, ProductInfo, Parameter, ProductParameter
from .serializers import ProductInfoSerializer

from yaml import load
from yaml.parser import ParserError
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader


class GoodsUploadAPIView(APIView):
    """Класс для загрузки товаров поставщиком"""
    permission_classes = [
        IsProvider,
    ]

    def post(self, request, *args, **kwargs):
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


class ProductInfoListAPIView(generics.ListAPIView):
    """Класс отображения списка товаров"""
    queryset = ProductInfo.objects.all()
    serializer_class = ProductInfoSerializer


class ProductInfoRetrieveAPIView(generics.RetrieveAPIView):
    """Класс отображения карточки товара"""
    queryset = ProductInfo.objects.all()
    serializer_class = ProductInfoSerializer
