from datetime import datetime

from rest_framework import status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response

from app.catalog.models import Brand, Product
from app.catalog.serializers.v0_1.serializers import (
    BrandSerializer,
    CreateProductSerializer,
    ProductSerializer,
)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    product_serializer = ProductSerializer
    create_product_serializer = CreateProductSerializer
    authentication_classes = [TokenAuthentication]

    def get_permissions(self):
        print(self.action)
        if self.action in ("create", "partial_update", "destroy"):
            return [IsAdminUser()]
        else:
            return [AllowAny()]

    def get_serializer_class(self):
        if self.action == "create":
            return CreateProductSerializer
        return ProductSerializer

    def perform_create(self, serializer):
        brand_id = self.request.data.get("brand_id")
        serializer.save(brand_id=brand_id)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.deleted:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.deleted:
            return Response(
                {"message": "Product is already deleted or not exists"},
                status=status.HTTP_404_NOT_FOUND,
            )

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
