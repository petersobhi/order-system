from djmoney.contrib.django_rest_framework import MoneyField
from rest_framework import serializers

from core.models import Category, Product, Order, OrderItem


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    converted_price = MoneyField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ('seller',)


class ProductPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        user = self.context['request'].user
        return Product.objects.exclude(seller=user)


class OrderPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        user = self.context['request'].user
        return Order.objects.filter(buyer=user)


class OrderItemSerializer(serializers.ModelSerializer):
    product_id = ProductPrimaryKeyRelatedField(source='product')
    product = ProductSerializer(read_only=True)
    order_id = OrderPrimaryKeyRelatedField(source='order')

    class Meta:
        model = OrderItem
        fields = '__all__'
        read_only_fields = ('price', 'order')


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(source='orderitem_set', many=True, read_only=True)

    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ('total_amount', 'status', 'buyer')
