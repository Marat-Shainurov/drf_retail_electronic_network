from django.db import transaction
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from products.models import Product
from sales_network.models import SoleProprietor, ContactInfo, RetailNetwork
from sales_network.serializers import ContactInfoBaseSerializer, ProductCreateSerializer


class SoleProprietorSerializer(serializers.ModelSerializer):
    class Meta:
        model = SoleProprietor
        fields = ('id', 'main_network', 'name', 'contact_info', 'products', 'factory_supplier',
                  'retail_network_supplier', 'debt_to_supplier', 'created_at', 'is_active')


class SoleProprietorCreateSerializer(serializers.ModelSerializer):
    contact_info = ContactInfoBaseSerializer(many=False, required=True)
    new_products = ProductCreateSerializer(many=True, required=False)
    product_ids_to_add = serializers.ListSerializer(child=serializers.IntegerField(), required=False)

    class Meta:
        model = SoleProprietor
        fields = ('main_network', 'name', 'contact_info', 'new_products', 'product_ids_to_add', 'factory_supplier',
                  'retail_network_supplier',)

    def create(self, validated_data):
        with transaction.atomic():
            contact_info_data = validated_data.pop('contact_info')
            new_products_data = validated_data.pop('new_products', [])
            product_ids_to_add_data = validated_data.pop('product_ids_to_add', [])
            contacts = ContactInfo(**contact_info_data)
            contacts.save()
            sole_proprietor = SoleProprietor.objects.create(**validated_data, contact_info=contacts)

            for product in new_products_data:
                sole_proprietor.products.create(**product)

            for product_id in product_ids_to_add_data:
                try:
                    product = get_object_or_404(Product, pk=product_id)
                    sole_proprietor.products.add(product)
                except Http404:
                    raise serializers.ValidationError(f'Product with "{product_id}" id not found')

            return sole_proprietor


class SoleProprietorUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SoleProprietor
        fields = ('name', 'contact_info', 'product_ids_to_add', 'product_ids_to_remove', 'factory_supplier',
                  'retail_network_supplier', 'is_active',)
