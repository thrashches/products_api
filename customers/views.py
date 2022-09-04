from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED
from django.contrib.auth import get_user_model, authenticate
from .serializers import UserSerializer, LoginSerializer, ConfirmSerializer
from .tasks import send_email_task
from .models import EmailConfirmToken


User = get_user_model()


class CustomersViewset(viewsets.GenericViewSet):
    """Вьюсет для работы с пользователями"""
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=['post'])
    def register(self, request):
        """Регистрация пользователя"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=HTTP_201_CREATED)

    def perform_create(self, serializer):
        user = serializer.save()
        email_token = EmailConfirmToken.objects.create(user_id=user.id)
        send_email_task.delay(
            email=user.email,
            subject='Подтверждение регистрации',
            message=email_token.token
        )

    @action(detail=False, methods=['post'], serializer_class=ConfirmSerializer)
    def confirm(self, request):
        """Подтверждение email пользователя"""
        if {'email', 'token'}.issubset(request.data):
            token = EmailConfirmToken.objects.filter(
                token=request.data.get('token')
            ).first()
            user = token.user
            if token and user.email == request.data.get('email'):
                user.is_active = True
                user.save()
                token.delete()
                return Response(
                    {'info': 'Пользователь успешно активирован!'},
                    status=HTTP_201_CREATED
                )
            else:
                return Response(
                    {'error': 'Неверный токен или email!'},
                    status=HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                {'error': 'Неверный формат запроса!'},
                status=HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=['post'], serializer_class=LoginSerializer)
    def login(self, request):
        """Вход в систему"""
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
