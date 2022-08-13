from rest_framework import serializers
from .models import Contact
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


User = get_user_model()


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        exclude = ['user']


class UserSerializer(serializers.ModelSerializer):
    password_1 = serializers.CharField(write_only=True)
    password_2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'last_name',
            'first_name',
            'patronymic',
            'email',
            'password_1',
            'password_2',
            'company',
            'position',
        ]

    def validate(self, data):
        """Дополнительная валидация паролей"""
        password_1 = data.pop('password_1')
        password_2 = data.pop('password_2')

        if password_1 and password_2 and password_1 != password_2:
            raise ValidationError('Пароли не совпадают!')
        validate_password(password_1)
        data['password'] = password_1
        return data

    def create(self, validated_data):
        """Сохранение пароля пользователя"""
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user
