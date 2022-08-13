from django.urls import path
from .views import LoginAPIView, UserRegistrationAPIView


app_name = 'customers'


urlpatterns = [
    path('register/', UserRegistrationAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
]