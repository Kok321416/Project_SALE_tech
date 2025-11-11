from rest_framework import serializers

from .models import NetworkNode, Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ("id", "name", "model", "release_date")
        read_only_fields = ("id",)


class NetworkNodeSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)
    level = serializers.IntegerField(read_only=True)

    class Meta:
        model = NetworkNode
        fields = (
            "id",
            "name",
            "email",
            "country",
            "city",
            "street",
            "house_number",
            "supplier",
            "debt",
            "level",
            "created_at",
            "products",
        )
        read_only_fields = ("id", "level", "created_at", "products")

    def update(self, instance, validated_data):
        if "debt" in validated_data:
            raise serializers.ValidationError({"debt": "Поле нельзя изменять через API."})
        return super().update(instance, validated_data)



