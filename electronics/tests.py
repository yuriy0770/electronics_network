from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from django.utils import timezone
from .models import Contact, Product, NetworkNode


class ContactModelTest(TestCase):
    def test_contact_creation(self):
        contact = Contact.objects.create(
            email="test@example.com",
            country="Россия",
            city="Москва",
            street="Тестовая",
            house_number="1"
        )
        self.assertEqual(contact.email, "test@example.com")
        self.assertEqual(contact.country, "Россия")
        self.assertEqual(contact.city, "Москва")


class ProductModelTest(TestCase):
    def test_product_creation(self):
        product = Product.objects.create(
            name="Тестовый продукт",
            model="T100",
            release_date=timezone.now().date()
        )
        self.assertEqual(product.name, "Тестовый продукт")
        self.assertEqual(product.model, "T100")


class NetworkNodeModelTest(TestCase):
    def setUp(self):
        self.contact = Contact.objects.create(
            email="factory@test.com",
            country="Россия",
            city="Москва",
            street="Заводская",
            house_number="1"
        )

        self.factory = NetworkNode.objects.create(
            name="Тестовый завод",
            node_type="factory",
            contact=self.contact
        )

    def test_network_node_creation(self):
        self.assertEqual(self.factory.name, "Тестовый завод")
        self.assertEqual(self.factory.node_type, "factory")
        self.assertEqual(self.factory.level, 0)

    def test_hierarchy_level(self):
        contact2 = Contact.objects.create(
            email="retail@test.com",
            country="Россия",
            city="СПб",
            street="Невский",
            house_number="2"
        )

        retail = NetworkNode.objects.create(
            name="Розничная сеть",
            node_type="retail",
            contact=contact2,
            supplier=self.factory
        )

        self.assertEqual(retail.level, 1)


class APIAuthenticationTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            is_active=True
        )
        self.client = APIClient()

        self.contact = Contact.objects.create(
            email="api@test.com",
            country="Россия",
            city="Москва",
            street="API тест",
            house_number="10"
        )

        self.factory = NetworkNode.objects.create(
            name="API Тестовый завод",
            node_type="factory",
            contact=self.contact
        )

    def test_api_requires_authentication(self):
        response = self.client.get('/api/network-nodes/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_api_with_authentication(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/network-nodes/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class StringRepresentationTest(TestCase):

    def test_product_str(self):
        product = Product.objects.create(
            name="Смартфон",
            model="X100",
            release_date=timezone.now().date()
        )
        self.assertEqual(str(product), "Смартфон (X100)")

    def test_network_node_str(self):
        contact = Contact.objects.create(
            email="node@test.com",
            country="Россия",
            city="Москва",
            street="Тест",
            house_number="1"
        )
        node = NetworkNode.objects.create(
            name="Тестовый узел",
            node_type="factory",
            contact=contact
        )
        self.assertIn("Тестовый узел", str(node))