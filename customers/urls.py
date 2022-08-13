from django.urls import path
from .views import LoginAPIView, UserRegistrationAPIView, UserConfirmView


app_name = 'customers'


urlpatterns = [
    path('register/', UserRegistrationAPIView.as_view(), name='register'),
    path('confirm/', UserConfirmView.as_view(), name='confirm'),
    path('login/', LoginAPIView.as_view(), name='login'),
]
