from rest_framework import routers

from app.catalog.viewsets.v0_1.viewsets import BrandViewSet, ProductViewSet
from app.users.viewsets.v0_1.viewsets import LoginViewSet, UserViewSet

router = routers.DefaultRouter(trailing_slash=True)

router.register(r"login", LoginViewSet, basename="login")
router.register(r"users", UserViewSet, basename="users")
router.register(r"products", ProductViewSet, basename="products")
router.register(r"brands", BrandViewSet, basename="brands")
