import os
from rest_framework.test import APITestCase
from django.conf import settings
from .models import Order
from customers.models import User
from goods.models import ProductInfo


class OrderSetupMixin:
    basket_url = '/api/v1/orders/basket/'

    @classmethod
    def setUpTestData(cls):
        test_buyer_data = {
            "last_name": "Иванов",
            "first_name": "Дмитрий",
            "patronymic": "Иванович",
            "company": "Яндекс",
            "position": "Топ менеджер",
            "email": "buyer@example.com",
            "is_active": True,
        }
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
        User.objects.create(**test_buyer_data)
        User.objects.create(**test_provider_data)

    def setUp(self):
        provider = User.objects.get(email='provider@example.com')
        self.client.force_login(provider)
        test_file_path = os.path.join(
            settings.BASE_DIR, 'test_data', 'shop1.yml')
        with open(test_file_path, 'r', encoding='utf-8') as f:
            self.client.post(
                path='/api/v1/goods/upload/',
                data={
                    'data': f,
                    'url': 'https://www.svyaznoy.ru/'
                },
                format='multipart'
            )
        self.client.logout()


class BasketAPITestCase(OrderSetupMixin, APITestCase):
    def test_basket_permissions(self):
        unauthorized_response = self.client.get(path=self.basket_url)
        self.assertEqual(unauthorized_response.status_code, 401)

    def test_basket_autocreation(self):
        user = User.objects.get(email="buyer@example.com")
        self.client.force_login(user)
        response = self.client.get(path=self.basket_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Order.objects.filter(
            user=user, status='basket').count(), 1)

    def test_basket_put_item(self):
        product_1 = ProductInfo.objects.get(article_number=4216292)
        product_2 = ProductInfo.objects.get(article_number=4216313)
        buyer = User.objects.get(email='buyer@example.com')
        self.client.force_login(buyer)

        basket_create_response = self.client.get(path=self.basket_url)
        self.assertEqual(basket_create_response.status_code, 200)

        response = self.client.put(
            path=self.basket_url,
            data={
                'items': [
                    {
                        'product_info': product_1.id,
                        'quantity': 2
                    },
                    {
                        'product_info': product_2.id,
                        'quantity': 1
                    }
                ]
            },
            format='json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['order_items']), 2)
        self.assertEqual(int(response.data['total']), 285000)

    def test_basket_remove_item(self):
        product_1 = ProductInfo.objects.get(article_number=4216292)
        buyer = User.objects.get(email='buyer@example.com')
        self.client.force_login(buyer)

        basket_create_response = self.client.get(path=self.basket_url)
        self.assertEqual(basket_create_response.status_code, 200)

        put_response = self.client.put(
            path=self.basket_url,
            data={
                'items': [
                    {
                        'product_info': product_1.id,
                        'quantity': 2
                    }
                ]
            },
            format='json'
        )
        self.assertEqual(put_response.status_code, 200)

        delete_response = self.client.delete(
            path=self.basket_url,
            data={
                'items': [1]
            },
            format='json'
        )

        self.assertEqual(delete_response.status_code, 200)
        self.assertEqual(len(delete_response.data['order_items']), 0)


class OrderAPITestCase(OrderSetupMixin, APITestCase):
    def test_order_confirm(self):
        product_1 = ProductInfo.objects.get(article_number=4216292)
        buyer = User.objects.get(email='buyer@example.com')
        self.client.force_login(buyer)

        basket_create_response = self.client.get(path=self.basket_url)
        self.assertEqual(basket_create_response.status_code, 200)

        put_response = self.client.put(
            path=self.basket_url,
            data={
                'items': [
                    {
                        'product_info': product_1.id,
                        'quantity': 2
                    }
                ]
            },
            format='json'
        )
        self.assertEqual(put_response.status_code, 200)
        order_id = put_response.data['id']

        confirm_response = self.client.post(
            path=f'/api/v1/orders/{order_id}/confirm/',
            data={
                'contact_data': {
                    'contact_type': 'Адрес',
                    'value': '127001, город Москва, улица Ленина, 15'
                }
            },
            format='json'
        )
        self.assertEqual(confirm_response.status_code, 201)
        order = Order.objects.get(id=order_id)
        self.assertEqual(order.status, 'new')

    def test_order_confirm_permissions(self):
        product_1 = ProductInfo.objects.get(article_number=4216292)
        buyer = User.objects.get(email='buyer@example.com')
        self.client.force_login(buyer)

        basket_create_response = self.client.get(path=self.basket_url)
        self.assertEqual(basket_create_response.status_code, 200)

        put_response = self.client.put(
            path=self.basket_url,
            data={
                'items': [
                    {
                        'product_info': product_1.id,
                        'quantity': 2
                    }
                ]
            },
            format='json'
        )
        self.assertEqual(put_response.status_code, 200)
        order_id = put_response.data['id']

        provider = User.objects.get(email='provider@example.com')
        self.client.force_login(provider)
        confirm_response = self.client.post(
            path=f'/api/v1/orders/{order_id}/confirm/',
            data={
                'contact_data': {
                    'contact_type': 'Адрес',
                    'value': '127001, город Москва, улица Ленина, 15'
                }
            },
            format='json'
        )
        self.assertNotEqual(confirm_response.status_code, 201)
