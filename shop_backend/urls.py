"""shop_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from goods.views import ProductInfoViewset
from customers.views import CustomersViewset
from orders.views import OrderViewset
from rest_framework.schemas import get_schema_view
from django.views.generic import TemplateView

router = DefaultRouter()
router.register('goods', ProductInfoViewset)
router.register('customers', CustomersViewset)
router.register('orders', OrderViewset)

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api/v1/orders/', include('orders.urls', namespace='orders')),
    path('api/v1/', include(router.urls)),
    path('openapi/', get_schema_view(
        title="Документация к API. Версия 1.",
        description="",
        version="1.0.0"
    ), name='openapi-schema'),
    path('swagger/', TemplateView.as_view(
        template_name='swagger.html',
        extra_context={'schema_url': 'openapi-schema'}
    ), name='swagger-ui'),
]
