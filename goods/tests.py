from http import client
import os
from rest_framework.test import APITestCase
from customers.models import User
from .models import ProductInfo, Shop
from django.conf import settings


class GoodsAPITestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        test_provider_data = {
            "last_name": "Иванов",
            "first_name": "Дмитрий",
            "patronymic": "Иванович",
            "company": "Яндекс",
            "position": "Топ менеджер",
            "email": "provider@example.com",
            "is_active": True,
            "user_type": "provider"
        }
        test_buyer_data = {
            "last_name": "Иванов",
            "first_name": "Дмитрий",
            "patronymic": "Иванович",
            "company": "Яндекс",
            "position": "Топ менеджер",
            "email": "buyer@example.com",
            "is_active": True,
        }
        User.objects.create(**test_provider_data)
        User.objects.create(**test_buyer_data)

    def test_goods_upload_by_provider(self):
        provider = User.objects.get(email='provider@example.com')
        self.client.force_login(provider)
        test_file_path = os.path.join(
            settings.BASE_DIR, 'test_data', 'shop1.yml')
        with open(test_file_path, 'r', encoding='utf-8') as f:
            provider_response = self.client.post(
                path='/api/v1/goods/upload/',
                data={
                    'data': f,
                    'url': 'https://www.svyaznoy.ru/'
                },
                format='multipart'
            )
            self.assertEqual(provider_response.status_code, 201)
        shop = Shop.objects.first()
        self.assertEqual(shop.url, 'https://www.svyaznoy.ru/')
        self.assertEqual(ProductInfo.objects.count(), 4)

    def test_goods_upload_by_buyer(self):
        buyer = User.objects.get(email='buyer@example.com')
        self.client.force_login(buyer)
        test_file_path = os.path.join(
            settings.BASE_DIR, 'test_data', 'shop1.yml')
        with open(test_file_path, 'r', encoding='utf-8') as f:
            buyer_response = self.client.post(
                path='/api/v1/goods/upload/',
                data={
                    'data': f,
                    'url': 'https://www.svyaznoy.ru/'
                },
                format='multipart'
            )
            self.assertEqual(buyer_response.status_code, 403)
