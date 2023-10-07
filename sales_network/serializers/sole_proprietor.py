from django.db import transaction, IntegrityError
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from products.models import Product
from products.serializers import ProductCreateSerializer
from sales_network.models import SoleProprietor, ContactInfo
from sales_network.serializers import (ContactInfoBaseSerializer, FactorySupplierSerializer,
                                       RetailNetSupplierSerializer, MainNetworkBaseSerializer)


class SoleProprietorSerializer(serializers.ModelSerializer):
    contact_info = ContactInfoBaseSerializer(read_only=True)
    factory_supplier = FactorySupplierSerializer(read_only=True)
    retail_network_supplier = RetailNetSupplierSerializer(read_only=True)
    main_network = MainNetworkBaseSerializer(read_only=True)

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
        fields = (
            'id', 'main_network', 'name', 'contact_info', 'new_products', 'product_ids_to_add', 'factory_supplier',
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
    name = serializers.CharField(required=False)
    contact_info_id = serializers.IntegerField(required=False)
    product_ids_to_add = serializers.ListSerializer(child=serializers.IntegerField(), required=False)
    product_ids_to_remove = serializers.ListSerializer(child=serializers.IntegerField(), required=False)

    class Meta:
        model = SoleProprietor
        fields = ('name', 'contact_info_id', 'product_ids_to_add', 'product_ids_to_remove', 'factory_supplier',
                  'retail_network_supplier', 'is_active',)

    def update(self, sole_proprietor, validated_data):
        with transaction.atomic():
            contact_info_data = validated_data.pop('contact_info_id', None)
            if contact_info_data:
                try:
                    new_contacts = get_object_or_404(ContactInfo, pk=contact_info_data)
                    sole_proprietor.contact_info = new_contacts
                except Http404:
                    raise serializers.ValidationError(f'ContactInfo with "{contact_info_data}" id not found')

            prod_ids_to_add_data = validated_data.pop('product_ids_to_add', [])
            for product_id in prod_ids_to_add_data:
                try:
                    prod_to_add = get_object_or_404(Product, pk=product_id)
                    sole_proprietor.products.add(prod_to_add)
                except Http404:
                    raise serializers.ValidationError(f'Product with "{product_id}" id not found')

            prod_ids_to_remove_data = validated_data.pop('product_ids_to_remove', [])
            for product_id in prod_ids_to_remove_data:
                try:
                    prod_to_remove = get_object_or_404(Product, pk=product_id)
                    if prod_to_remove not in sole_proprietor.products.all():
                        raise serializers.ValidationError(
                            f"The {product_id} product is not related to {sole_proprietor}")
                    sole_proprietor.products.remove(prod_to_remove)
                except Http404:
                    raise serializers.ValidationError(f'Product with "{product_id}" id not found')

            for attr, val in validated_data.items():
                setattr(sole_proprietor, attr, val)

            try:
                sole_proprietor.save()
            except IntegrityError:
                raise serializers.ValidationError(
                    f'ContactInfo with "{contact_info_data}" id is already related to another entity.')
            return sole_proprietor
