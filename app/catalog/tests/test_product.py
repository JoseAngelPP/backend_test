from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from app.catalog.models import Brand, Product
from app.users.models import User


class ProductViewSetTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.group = Group.objects.create(name="tests")
        self.admin_user = User.objects.create(
            username="admin",
            password="adminpass",
            groups=self.group,
            is_superuser=True,
            is_staff=True,
        )
        self.brand = Brand.objects.create(
            name="TestBrand", description="TestDescription"
        )
        self.token, _ = Token.objects.get_or_create(user=self.admin_user)
        self.headers = {"Authorization": f"Token {self.token}"}

    def create_product(self):
        return Product.objects.create(
            name="TestProduct",
            description="TestDescription",
            brand=self.brand,
            sku="TestSKU",
            price=10.0,
        )

    def test_create_product(self):
        url = reverse("api:products-list")
        data = {
            "name": "NewProduct",
            "description": "NewDescription",
            "brand_id": self.brand.id,
            "sku": "NewSKU",
            "price": 20.0,
        }

        response = self.client.post(
            path=url, headers=self.headers, data=data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(Product.objects.get().name, "NewProduct")

    def test_partial_update_product(self):
        product = self.create_product()
        url = reverse("api:products-detail", args=[product.id])
        data = {"name": "UpdatedProduct"}

        response = self.client.patch(
            path=url, headers=self.headers, data=data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        product.refresh_from_db()
        self.assertEqual(product.name, "UpdatedProduct")

    def test_destroy_product(self):
        product = self.create_product()
        url = reverse("api:products-detail", args=[product.id])

        response = self.client.delete(path=url, headers=self.headers, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        product.refresh_from_db()
        self.assertIsNotNone(product.deleted)

    def test_fail_create_product_not_authorized(self):
        url = reverse("api:products-list")
        data = {
            "name": "NewProduct",
            "description": "NewDescription",
            "brand_id": self.brand.id,
            "sku": "NewSKU",
            "price": 20.0,
        }

        response = self.client.post(path=url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_fail_partial_update_product_not_authorized(self):
        product = self.create_product()
        url = reverse("api:products-detail", args=[product.id])
        data = {"name": "UpdatedProduct"}

        response = self.client.patch(path=url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_fail_destroy_product_not_authorized(self):
        product = self.create_product()
        url = reverse("api:products-detail", args=[product.id])

        response = self.client.delete(path=url, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        product.refresh_from_db()
        self.assertIsNone(product.deleted)
