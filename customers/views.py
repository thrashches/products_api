from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED
from django.contrib.auth import get_user_model, authenticate
from .serializers import UserSerializer


User = get_user_model()


class UserRegistrationAPIView(generics.CreateAPIView):
    """Регистрация пользователя"""
    queryset = User.objects.all()
    serializer_class = UserSerializer


class LoginAPIView(APIView):
    """Вход в систему"""

    def post(self, request, *args, **kwargs):
        if {'email', 'password'}.issubset(request.data):
            user = authenticate(
                request,
                username=request.data.get('email'),
                password=request.data.get('password')
            )

            if user is not None:
                if user.is_active:
                    token, created = Token.objects.get_or_create(user=user)
                    return Response(
                        {'info': 'Вы успешно авторизовались!', 'token': token.key},
                        status=HTTP_201_CREATED
                    )
                else:
                    return Response(
                        {'error': 'Пользователь не активен!'},
                        status=HTTP_401_UNAUTHORIZED
                    )
            else:
                return Response(
                    {'error': 'Неверные учетные данные!'},
                    status=HTTP_401_UNAUTHORIZED
                )
        else:
            return Response(
                {'error': 'Неверный формат запроса!'},
                status=HTTP_400_BAD_REQUEST
            )
