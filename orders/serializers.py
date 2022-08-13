from rest_framework import serializers
from .models import Order, OrderItem
from goods.serializers import ProductInfoSerializer


class OrderItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = [
            'product_info',
            'quantity',
        ]


class OrderItemSerializer(serializers.ModelSerializer):
    product_info = ProductInfoSerializer(write_only=True)
    name = serializers.SerializerMethodField()
    shop = serializers.SerializerMethodField()
    total = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = [
            'id',
            'name',
            'shop',
            'product_info',
            'quantity',
            'total',
        ]

    def get_name(self, obj):
        return obj.product_info.name

    def get_shop(self, obj):
        return obj.product_info.shop.name

    def get_total(self, obj):
        return obj.product_info.price * obj.quantity


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)
    total = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = [
            'id',
            'date_time',
            'user',
            'order_items',
        ]

    def create(self, validated_data):
        user = self.context['request'].user
        print(user)
        return super().create(validated_data)

    def get_total(self, obj):
        total = 0
        for item in obj.order_items.all():
            total_item = item.product_info.price * item.quantity
            total += total_item
        return total
