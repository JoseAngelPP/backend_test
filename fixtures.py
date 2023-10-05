import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings.base")

import django

django.setup()
import random

from django.contrib.auth.models import Group

from app.catalog.models import Brand, Product
from app.users.models import User

admin_group, created = Group.objects.get_or_create(name="admin")

User.objects.get_or_create(
    username="admin",
    password="123",
    groups=admin_group,
    is_superuser=True,
    is_staff=True,
)

print("User created")

brands_data = [
    {"name": "Brand1", "description": "Description1"},
    {"name": "Brand2", "description": "Description2"},
]

for brand_data in brands_data:
    Brand.objects.get_or_create(**brand_data)

print("Brands created")


products_data = []
for i in range(20):
    brand = Brand.objects.get(id=random.randint(1, 2))
    product_data = {
        "name": f"Product {i}",
        "description": f"Description product {i}",
        "brand": brand,
        "sku": f"sku{i}_{i}",
        "price": round(random.uniform(10, 100), 2),
    }
    products_data.append(product_data)

products = []
for product_data in products_data:
    product = Product.objects.get_or_create(**product_data)
    products.append(product)

print("Products created")
