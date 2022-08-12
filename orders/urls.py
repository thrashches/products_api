from django.urls import path
from .views import OrderRetrieveAPIView, BasketAPIView, OrderConfirmAPIView, OrderListAPIView


app_name = 'orders'


urlpatterns = [
    path('', OrderListAPIView.as_view(), name='list'),
    path('basket/', BasketAPIView.as_view(), name='basket'),
    path('<int:pk>/', OrderRetrieveAPIView.as_view(), name='retrieve'),
    path('<int:pk>/confirm/', OrderConfirmAPIView.as_view(), name='confirm'),
]
