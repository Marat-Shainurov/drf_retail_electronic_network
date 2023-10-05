from django.db import transaction
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from products.models import Product
from sales_network.models import RetailNetwork, ContactInfo
from sales_network.serializers import ProductCreateSerializer, ContactInfoBaseSerializer


class RetailNetSerializer(serializers.ModelSerializer):
    class Meta:
        model = RetailNetwork
        fields = ('id', 'main_network', 'name', 'contact_info', 'products', 'factory_supplier', 'debt_to_supplier',
                  'created_at', 'is_active')


class RetailNetCreateSerializer(serializers.ModelSerializer):
    contact_info = ContactInfoBaseSerializer(many=False, required=True)
    new_products = ProductCreateSerializer(many=True, required=False)
    product_ids_to_add = serializers.ListSerializer(child=serializers.IntegerField(), required=False)

    class Meta:
        model = RetailNetwork
        fields = ('main_network', 'name', 'contact_info', 'new_products', 'product_ids_to_add', 'factory_supplier',)

    def create(self, validated_data):
        with transaction.atomic():
            contact_info_data = validated_data.pop('contact_info')
            new_products_data = validated_data.pop('new_products', [])
            product_ids_to_add_data = validated_data.pop('product_ids_to_add', [])
            contacts = ContactInfo(**contact_info_data)
            contacts.save()
            retail_network = RetailNetwork.objects.create(**validated_data, contact_info=contacts)

            for product in new_products_data:
                retail_network.products.create(**product)

            for product_id in product_ids_to_add_data:
                try:
                    product = get_object_or_404(Product, pk=product_id)
                    retail_network.products.add(product)
                except Http404:
                    raise serializers.ValidationError(f'Product with "{product_id}" id not found')

            return retail_network


class RetailNetUpdateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False)
    contact_info_id = serializers.IntegerField(required=False)
    product_ids_to_add = serializers.ListField(child=serializers.IntegerField(), required=False)
    product_ids_to_remove = serializers.ListSerializer(child=serializers.IntegerField(), required=False)

    class Meta:
        model = RetailNetwork
        fields = ('id', 'name', 'contact_info_id', 'product_ids_to_add', 'product_ids_to_remove', 'factory_supplier',
                  'is_active',)

    def update(self, retail_network, validated_data):
        with transaction.atomic():
            contact_info_data = validated_data.pop('contact_info_id', None)
            if contact_info_data:
                try:
                    new_contacts = get_object_or_404(ContactInfo, pk=contact_info_data)
                    retail_network.contact_info = new_contacts
                except Http404:
                    raise serializers.ValidationError(f'ContactInfo with "{contact_info_data}" id not found')

            prod_ids_to_add_data = validated_data.pop('product_ids_to_add', [])
            for product_id in prod_ids_to_add_data:
                try:
                    prod_to_add = get_object_or_404(Product, pk=product_id)
                    retail_network.products.add(prod_to_add)
                except Http404:
                    raise serializers.ValidationError(f'Product with "{product_id}" id not found')

            prod_ids_to_remove_data = validated_data.pop('product_ids_to_remove', [])
            for product_id in prod_ids_to_remove_data:
                try:
                    prod_to_remove = get_object_or_404(Product, pk=product_id)
                    if prod_to_remove not in retail_network.products.all():
                        raise serializers.ValidationError(f"The {product_id} product is not related to {retail_network}")
                    retail_network.products.remove(prod_to_remove)
                except Http404:
                    raise serializers.ValidationError(f'Product with "{product_id}" id not found')

            for attr, val in validated_data.items():
                setattr(retail_network, attr, val)

            retail_network.save()
            return retail_network
