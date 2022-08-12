from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from orders.serializers import OrderSerializer, OrderItemSerializer
from .models import Order, OrderItem


class OrderRetrieveAPIView(generics.RetrieveAPIView):
    """Отображение заказа"""
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class BasketAPIView(APIView):
    """Работа с корзиной"""
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def get(self, request, *args, **kwargs):
        """Получение корзины пользователя"""
        basket = Order.objects.filter(user=request.user, status='basket').last()
        if not basket:
            # Если у пользователя нет корзины, то создаем пустую автоматически
            basket = Order.objects.create(user=request.user, status='basket')
        serializer = OrderSerializer(basket)
        return Response(serializer.data, status=HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        """Добавление товаров в корзину"""
        if items := request.data.get('items'):
            serializer = OrderItemSerializer(data=items)
            if serializer.is_valid():
                pass

