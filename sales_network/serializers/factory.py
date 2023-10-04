from rest_framework import serializers

from products.models import Product
from sales_network.models import Factory, ContactInfo
from sales_network.serializers import ProductBaseSerializer, ContactInfoBaseSerializer, ProductCreateSerializer


class FactorySerializer(serializers.ModelSerializer):
    contact_info = ContactInfoBaseSerializer(many=False, read_only=True)
    products = ProductBaseSerializer(many=True, read_only=True)

    class Meta:
        model = Factory
        fields = ('id', 'name', 'contact_info', 'products', 'created_at', 'is_active')


class FactoryCreateSerializer(serializers.ModelSerializer):
    contact_info = ContactInfoBaseSerializer(many=False, required=True)
    products = ProductCreateSerializer(many=True, required=False)

    class Meta:
        model = Factory
        fields = ('name', 'contact_info', 'products',)

    def create(self, validated_data):
        contacts_data = validated_data.pop('contact_info')
        products_data = validated_data.pop('products', [])
        contacts = ContactInfo.objects.create(**contacts_data)
        factory = Factory.objects.create(**validated_data, contact_info=contacts)

        for product in products_data:
            factory.products.create(**product)

        return factory
