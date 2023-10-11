from datetime import datetime

from prometheus_client import Gauge
from rest_framework import status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response

from app.catalog.models import Brand, Product, ProductQuery
from app.catalog.serializers.v0_1.serializers import (
    BrandSerializer,
    CreateProductSerializer,
    ProductSerializer,
)
from app.catalog.utils import (
    send_new_product_add_email,
    send_product_deleted_email,
    send_product_updated_email,
)

products_views_total = Gauge("requests_total", "Total number of views")


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    product_serializer = ProductSerializer
    create_product_serializer = CreateProductSerializer
    authentication_classes = [TokenAuthentication]

    def get_permissions(self):
        if self.action in ("create", "partial_update", "destroy"):
            return [IsAdminUser()]
        else:
            return [AllowAny()]

    def get_serializer_class(self):
        if self.action == "create":
            return CreateProductSerializer
        return ProductSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        extra_data = {
            "ip": self.request.META.get("REMOTE_ADDR", None),
            "user_agent": self.request.META.get("HTTP_USER_AGENT", None),
        }
        products_views_total.inc()

        ProductQuery.objects.create(product=instance, extra_data=extra_data)
        return Response(serializer.data)

    def perform_create(self, serializer):
        brand_id = self.request.data.get("brand_id")
        instance = serializer.save(brand_id=brand_id)
        user = self.request.user
        send_new_product_add_email.delay(instance.pk, user.pk)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.deleted:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        user = self.request.user
        send_product_updated_email.delay(instance.pk, user.pk)
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.deleted:
            return Response(
                {"message": "Product is already deleted or not exists"},
                status=status.HTTP_404_NOT_FOUND,
            )

        user = self.request.user
        send_product_deleted_email.delay(instance.pk, user.pk)
        instance.deleted = datetime.now()
        instance.save()

        return Response(
            {"message": "Product deleted"}, status=status.HTTP_204_NO_CONTENT
        )


class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    authentication_classes = [TokenAuthentication]

    def get_permissions(self):
        if self.action in ("create", "partial_update", "destroy"):
            return [IsAdminUser()]
        else:
            return [AllowAny()]

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.deleted:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.deleted:
            return Response(
                {"message": "Brand is already deleted or not exists"},
                status=status.HTTP_404_NOT_FOUND,
            )

        instance.deleted = datetime.now()
        instance.save()

        return Response({"message": "Brand deleted"}, status=status.HTTP_204_NO_CONTENT)
