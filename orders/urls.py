from django.urls import path
from .views import OrderRetrieveAPIView, BasketAPIView


app_name = 'orders'


urlpatterns = [
    path('basket/', BasketAPIView.as_view(), name='basket'),
    path('<int:pk>/', OrderRetrieveAPIView.as_view(), name='retrieve'),
    # path('upload/', GoodsUploadAPIView.as_view(), name='upload'),
]
