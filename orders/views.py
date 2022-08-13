from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from customers.permissions import IsObjectOwner
from customers.serializers import ContactSerializer
from orders.serializers import OrderSerializer, OrderItemCreateSerializer
from django.shortcuts import get_object_or_404
from .models import Order, OrderItem
from customers.utils import send_email


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
        basket = Order.objects.filter(
            user=request.user, status='basket').last()
        if not basket:
            # Если у пользователя нет корзины, то создаем пустую автоматически
            basket = Order.objects.create(user=request.user, status='basket')
        serializer = OrderSerializer(basket)
        return Response(serializer.data, status=HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        """Добавление товаров в корзину, редактирование позиции"""
        basket = Order.objects.filter(
            user=request.user, status='basket').last()
        if items := request.data.get('items'):
            for item in items:
                serializer = OrderItemCreateSerializer(data=item)
                if serializer.is_valid():
                    order_item, created = OrderItem.objects.get_or_create(
                        order=basket, product_info_id=item['product_info']
                    )
                    order_item.quantity = item['quantity']
                    order_item.save()
                else:
                    return Response({'error': 'Неверный формат данных!'}, status=HTTP_400_BAD_REQUEST)
        basket_serializer = OrderSerializer(basket)
        return Response(basket_serializer.data, status=HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        """Удаление позиций из корзины"""
        if items := request.data.get('items'):
            OrderItem.objects.filter(id__in=items).delete()
        basket = Order.objects.filter(
            user=request.user, status='basket').last()
        basket_serializer = OrderSerializer(basket)
        return Response(basket_serializer.data, status=HTTP_200_OK)


class OrderConfirmAPIView(APIView):
    """Подтверждение заказа"""
    permission_classes = [
        IsObjectOwner,
    ]

    def post(self, request, *args, **kwargs):
        order_id = kwargs.get('pk')
        order = get_object_or_404(Order, id=order_id)
        contact_data = request.data.get('contact_data')
        serializer = ContactSerializer(data=contact_data)
        if serializer.is_valid():
            send_email(
                user=order.user,
                subject='Информация о вашем заказе',
                message='Ваш заказ был успешно оформлен!'
            )
            serializer.validated_data['user'] = request.user
            contact = serializer.save()
            order.contact = contact
            order.status = 'new'
            order.save()
            return Response({'info': 'Заказ успешно оформлен!'}, status=HTTP_201_CREATED)
        return Response({'error': 'Неверный формат контактных данных!'}, status=HTTP_400_BAD_REQUEST)


class OrderListAPIView(generics.ListAPIView):
    """Список заказов"""
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
