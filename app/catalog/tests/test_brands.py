from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from app.catalog.models import Brand
from app.users.models import User


class BrandViewSetTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.group = Group.objects.create(name="tests")
        self.admin_user = User.objects.create_user(
            username="admin",
            password="adminpass",
            groups=self.group,
            is_superuser=True,
            is_staff=True,
        )
        self.token, _ = Token.objects.get_or_create(user=self.admin_user)
        self.headers = {"Authorization": f"Token {self.token}"}

    def create_brand(self):
        return Brand.objects.create(name="TestBrand", description="TestDescription")

    def test_create_brand(self):
        url = reverse("api:brands-list")
        data = {"name": "NewBrand", "description": "NewDescription"}
        print(self.headers)

        response = self.client.post(
            path=url, headers=self.headers, data=data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Brand.objects.count(), 1)
        self.assertEqual(Brand.objects.get().name, "NewBrand")

    def test_destroy_brand(self):
        brand = self.create_brand()
        url = reverse("api:brands-detail", args=[brand.id])

        response = self.client.delete(path=url, headers=self.headers, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        brand.refresh_from_db()
        self.assertIsNotNone(brand.deleted)

    def test_fail_create_brand_not_authorized(self):
        url = reverse("api:brands-list")
        data = {"name": "NewBrand", "description": "NewDescription"}
        print(self.headers)

        response = self.client.post(path=url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_fail_destroy_brand_not_authorized(self):
        brand = self.create_brand()
        url = reverse("api:brands-detail", args=[brand.id])

        response = self.client.delete(path=url, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        brand.refresh_from_db()
        self.assertIsNone(brand.deleted)
