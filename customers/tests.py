from rest_framework import status
from rest_framework.test import APITestCase
from .models import User, EmailConfirmToken


class CustomersAPITestCase(APITestCase):
    def test_registration(self):
        response = self.client.post(
            path='/api/v1/customers/register/',
            data={
                "last_name": "Иванов",
                "first_name": "Дмитрий",
                "patronymic": "Иванович",
                "company": "Яндекс",
                "position": "Топ менеджер",
                "email": "ivanov_dmitry@example.com",
                "password_1": "Str0ngP@ssw0rd",
                "password_2": "Str0ngP@ssw0rd"
            },
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_data = {
            "last_name": "Иванов",
            "first_name": "Дмитрий",
            "patronymic": "Иванович",
            "company": "Яндекс",
            "position": "Топ менеджер",
            "email": "ivanov_dmitry@example.com"
        }
        self.assertEqual(response.data, response_data)
        self.assertEqual(User.objects.count(), 1)

    def test_register_validation(self):
        response = self.client.post(
            path='/api/v1/customers/register/',
            data={
                "last_name": "Иванов",
                "first_name": "Дмитрий",
                "patronymic": "Иванович",
                "company": "Яндекс",
                "position": "Топ менеджер",
                "email": "ivanov_dmitry@example.com",
                "password_1": "Str0ngP@s",
                "password_2": "Str0ngP@ssw0rd"
            },
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_confirm_token(self):
        self.client.post(
            path='/api/v1/customers/register/',
            data={
                "last_name": "Иванов",
                "first_name": "Дмитрий",
                "patronymic": "Иванович",
                "company": "Яндекс",
                "position": "Топ менеджер",
                "email": "ivanov_dmitry@example.com",
                "password_1": "Str0ngP@ssw0rd",
                "password_2": "Str0ngP@ssw0rd"
            },
            format='json'
        )
        user = User.objects.first()
        token = EmailConfirmToken.objects.get(user=user).token
        response = self.client.post(
            path='/api/v1/customers/confirm/',
            data={
                "email": "ivanov_dmitry@example.com",
                "token": token
            },
            format='json'
        )
        self.assertEqual(user.is_active, False)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user.refresh_from_db()
        self.assertEqual(user.is_active, True)
