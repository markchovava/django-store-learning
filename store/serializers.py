from rest_framework import serializers
from decimal import Decimal
from store.models import Product, Collection, Cart


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title', 'products_count']

    products_count = serializers.IntegerField(read_only=True)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'slug', 'inventory','unit_price', 'price_with_tax', 'collection']
    # id = serializers.IntegerField()
    # title = serializers.CharField(max_length=255)
    # price = serializers.DecimalField(max_digits=6, decimal_places=2, source='unit_price')
    price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')
    # collection = CollectionSerializer()
    # collection = serializers.HyperlinkedRelatedField(
    #    queryset=Collection.objects.all(),
    #    view_name='collection-detail'
    # )

    def calculate_tax(self, product: Product):
        return product.unit_price * Decimal(1.1)

    #   CUSTOM VALIDATION
    #  def validate(self, data):
    #    if data['password'] != data['confirm_password']:
    #        return serializers.ValidationError('Password do not match')
    #    return data

    
class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)

    class Meta:
        model = Cart
        fields = ['id'] 