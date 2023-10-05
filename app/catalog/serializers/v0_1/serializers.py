from rest_framework import serializers

from app.catalog.models import Brand, Product


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = (
            "id",
            "name",
            "description",
        )


class ProductSerializer(serializers.ModelSerializer):
    brand = BrandSerializer()

    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "description",
            "brand",
            "sku",
            "price",
        )


class CreateProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "description",
            "brand_id",
            "sku",
            "price",
        )
