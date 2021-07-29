from django.urls import reverse
from django.utils.module_loading import import_string
from djmoney import settings
from rest_framework import status
from rest_framework.test import APITestCase

from core.factories import UserFactory, ProductFactory, OrderFactory


def setup_exchange_rates():
    backend = import_string(settings.EXCHANGE_BACKEND)()
    backend.update_rates()


class ProductTests(APITestCase):
    def setUp(self):
        setup_exchange_rates()
        self.user = UserFactory(username='user')
        self.user2 = UserFactory(username='user2')
        self.admin = UserFactory(username='admin', is_staff=True)
        self.admin2 = UserFactory(username='admin2', is_staff=True)
        self.product = ProductFactory(seller=self.admin)
        self.url = reverse("product-list")
        self.detail_url = reverse("product-detail", kwargs={'pk': self.product.pk})
        self.product_data = {
            "title": "test product",
            "description": "test product",
            "price": 30,
            "price_currency": "EUR"
        }

    def test_list_products_as_unauthorized_user(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_products(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_product_as_normal_user(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, data=self.product_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_product_as_admin(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(self.url, data=self.product_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_modify_product_with_different_seller(self):
        self.client.force_authenticate(user=self.admin2)
        response = self.client.patch(self.detail_url, data=self.product_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_modify_product(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.patch(self.detail_url, data=self.product_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class OrderTests(APITestCase):
    def setUp(self):
        self.user = UserFactory(username='user')
        self.user2 = UserFactory(username='user2')
        self.admin = UserFactory(username='admin', is_staff=True)
        self.admin2 = UserFactory(username='admin2', is_staff=True)
        self.product = ProductFactory(seller=self.admin)
        self.order = OrderFactory(buyer=self.user)
        self.order2 = OrderFactory(buyer=self.admin)
        self.order_url = reverse("order-list")
        self.order_item_url = reverse("order-items")
        self.revenue_url = reverse("revenue")
        self.detail_url = reverse("product-detail", kwargs={'pk': self.product.pk})
        self.order_data = {
            "payment_method": "cod"
        }
        self.order_item_data = {
            "product_id": self.product.pk,
            "order_id": self.order.pk,
            "quantity": 3
        }
        self.order_item_data2 = {
            "product_id": self.product.pk,
            "order_id": self.order2.pk,
            "quantity": 3
        }

    def test_create_order(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.order_url, data=self.order_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_add_order_item(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.order_item_url, data=self.order_item_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_add_order_item_to_unowned_order(self):
        self.client.force_authenticate(user=self.user2)
        response = self.client.post(self.order_item_url, data=self.order_item_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add_own_product_to_order(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(self.order_item_url, data=self.order_item_data2)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_orders(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.order_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_revenue(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(self.revenue_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
