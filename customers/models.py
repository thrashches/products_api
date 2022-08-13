from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _
from .utils import generate_token


USER_TYPE_CHOICES = (
    ('provider', 'Поставщик'),
    ('buyer', 'Покупатель'),
)


class UserManager(BaseUserManager):
    """
    Мэнеджер пользователя
    """
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Создает и сохраняет пользователя с предоставленными 
        username, email, and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.is_active = True
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """
    Модель пользователя
    """
    REQUIRED_FIELDS = []
    objects = UserManager()
    USERNAME_FIELD = 'email'
    email = models.EmailField(_('email address'), unique=True)
    patronymic = models.CharField(
        max_length=255, blank=True, verbose_name='Отчество')
    company = models.CharField(
        verbose_name='Компания', max_length=40, blank=True)
    position = models.CharField(
        verbose_name='Должность', max_length=40, blank=True)
    username_validator = UnicodeUsernameValidator()
    username = None
    is_active = models.BooleanField(
        _('active'),
        default=False,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    user_type = models.CharField(verbose_name='Тип пользователя',
                                 choices=USER_TYPE_CHOICES, max_length=8, default='buyer')

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = "Список пользователей"
        ordering = ('email',)


class Contact(models.Model):
    class Meta:
        verbose_name = 'Контакт пользователя'
        verbose_name_plural = 'Контакты пользователей'

    contact_type = models.CharField(
        max_length=255, verbose_name='тип контактной информации')
    user = models.ForeignKey(
        User, verbose_name='пользователь', on_delete=models.CASCADE)
    value = models.CharField(max_length=500, verbose_name='значение')

    def __str__(self):
        return f'{self.user.email}: {self.contact_type}'


class EmailConfirmToken(models.Model):
    """Модель токена подтверждения пользователя"""
    class Meta:
        verbose_name = 'Токен подтверждения email'
        verbose_name_plural = 'Токены подтверждения email'

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='пользоватлеь')
    token = models.CharField(
        max_length=64,
        db_index=True,
        unique=True,
        verbose_name='токен'
    )

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = generate_token()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.user.email
