from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.serializers import ValidationError

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
    new_products = ProductCreateSerializer(many=True, required=False)
    products_ids_to_add = serializers.ListField(required=False)

    class Meta:
        model = Factory
        fields = ('name', 'main_network', 'contact_info', 'new_products', 'products_ids_to_add',)

    def create(self, validated_data):
        contacts_data = validated_data.pop('contact_info')
        new_products_data = validated_data.pop('new_products', [])
        prod_ids_list = validated_data.pop('products_ids_to_add', [])

        contacts = ContactInfo.objects.create(**contacts_data)
        factory = Factory.objects.create(**validated_data, contact_info=contacts)

        for p in new_products_data:
            factory.products.create(**p)

        for p in prod_ids_list:
            prod_to_add = get_object_or_404(Product, pk=p)
            factory.products.add(prod_to_add)

        return factory


class FactoryUpdateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False)
    contact_info_id = serializers.CharField(required=False)
    product_ids_to_add = serializers.ListField(child=serializers.IntegerField(), required=False)
    product_ids_to_remove = serializers.ListSerializer(child=serializers.IntegerField(), required=False)

    class Meta:
        model = Factory
        fields = ('name', 'contact_info_id', 'product_ids_to_add', 'product_ids_to_remove', 'is_active', 'products',)

    def update(self, factory, validated_data):
        contact_info_data = validated_data.pop('contact_info_id', None)
        if contact_info_data:
            try:
                new_contacts = get_object_or_404(ContactInfo, pk=contact_info_data)
                factory.contact_info = new_contacts
            except Http404:
                raise serializers.ValidationError(f'ContactInfo with "{contact_info_data}" id not found')

        prod_ids_to_add_data = validated_data.pop('product_ids_to_add', [])
        for p_id in prod_ids_to_add_data:
            try:
                prod_to_add = get_object_or_404(Product, pk=p_id)
                factory.products.add(prod_to_add)
            except Http404:
                raise serializers.ValidationError(f'Product with "{p_id}" id not found')

        prod_ids_to_remove_data = validated_data.pop('product_ids_to_remove', [])
        for p_id in prod_ids_to_remove_data:
            try:
                prod_to_remove = get_object_or_404(Product, pk=p_id)
                if prod_to_remove not in factory.products.all():
                    raise ValidationError(f"The {p_id} product is not related to {factory}")
                factory.products.remove(prod_to_remove)
            except Http404:
                raise serializers.ValidationError(f'Product with "{p_id}" id not found')

        for attr, val in validated_data.items():
            setattr(factory, attr, val)

        factory.save()
        return factory
