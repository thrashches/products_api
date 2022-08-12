from dataclasses import fields
from rest_framework import serializers
from .models import Product, ProductInfo, ProductParameter, Shop


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()

    class Meta:
        model = Product
        fields = [
            'name',
            'category',
        ]


class ProductParameterSerializer(serializers.ModelSerializer):
    parameter = serializers.StringRelatedField()

    class Meta:
        model = ProductParameter
        fields = [
            'parameter',
            'value',
        ]


class ProductInfoSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_parameters = ProductParameterSerializer(read_only=True, many=True)

    class Meta:
        model = ProductInfo
        fields = [
            'id',
            'shop',
            'product',
            'article_number',
            'model',
            'name',
            'quantity',
            'price',
            'price_rrc',
            'product_parameters',
        ]
