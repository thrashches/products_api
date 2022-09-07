from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from customers.permissions import IsObjectOwner
from customers.serializers import ContactSerializer
from orders.serializers import OrderSerializer, OrderItemCreateSerializer, BasketPutSerializer,\
    BasketRemoveSerializer, OrderConfirmSerializer, FailSerializer, SuccessSerializer
from django.shortcuts import get_object_or_404
from .models import Order, OrderItem
from customers.tasks import send_email_task
from drf_spectacular.utils import extend_schema, extend_schema_serializer, OpenApiExample


class OrderViewset(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """Вьюсет для работы с заказами и корзиной"""
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        """Отображение списка заказов"""
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """Отображение заказа"""
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        responses={200: OrderSerializer}
    )
    @action(detail=False, methods=['get'])
    def basket(self, request):
        basket = Order.objects.filter(
            user=request.user, status='basket').last()

        """Отображение корзины пользователя"""
        if not basket:
            # Если у пользователя нет корзины, то создаем пустую автоматически
            basket = Order.objects.create(
                user=request.user, status='basket')
        serializer = OrderSerializer(basket)
        return Response(serializer.data, status=HTTP_200_OK)

    @extend_schema(
        request=BasketPutSerializer,
        responses={200: OrderSerializer, 400: FailSerializer}
    )
    @basket.mapping.put
    def basket_put(self, request):
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

    @extend_schema(
        request=BasketRemoveSerializer,
        responses={200: OrderSerializer}
    )
    @basket.mapping.delete
    def basket_delete(self, request):
        """Удаление позиций из корзины"""
        basket = Order.objects.filter(
            user=request.user, status='basket').last()
        if items := request.data.get('items'):
            OrderItem.objects.filter(id__in=items).delete()
        basket_serializer = OrderSerializer(basket)
        return Response(basket_serializer.data, status=HTTP_200_OK)

    @extend_schema(
        request=OrderConfirmSerializer,
        responses={201: SuccessSerializer,
                   400: FailSerializer}
    )
    @action(detail=True, methods=['post'],
            permission_classes=[IsObjectOwner], serializer_class=OrderConfirmSerializer)
    def confirm(self, request, *args, **kwargs):
        """Подтверждение заказа"""
        order = self.get_object()
        contact_data = request.data.get('contact_data')
        serializer = ContactSerializer(data=contact_data)
        if serializer.is_valid():
            send_email_task.delay(
                email=order.user.email,
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
