from decimal import Decimal, ROUND_DOWN
from rest_framework import serializers
from .models import Product, Collection


class CollectionSerializer(serializers.Serializer):
    class Meta:
        model = Collection
        fields = ['id', 'title']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'unit_price', 'price_with_tax', 'collection']
    price_with_tax = serializers.SerializerMethodField(method_name="calculate_tax")

    def calculate_tax(self, product: Product):
        return product.unit_price * Decimal(1.1).quantize(Decimal('0.00'), rounding=ROUND_DOWN)

