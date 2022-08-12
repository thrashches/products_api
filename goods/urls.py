from django.urls import path
from .views import GoodsUploadAPIView, ProductInfoListAPIView, ProductInfoRetrieveAPIView


app_name = 'goods'


urlpatterns = [
    path('', ProductInfoListAPIView.as_view(), name='list'),
    path('<int:pk>/', ProductInfoRetrieveAPIView.as_view(), name='retrieve'),
    path('upload/', GoodsUploadAPIView.as_view(), name='upload'),
]
