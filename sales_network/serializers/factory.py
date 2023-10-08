from django.db import transaction, IntegrityError
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.serializers import ValidationError

from products.models import Product
from products.serializers import ProductBaseSerializer, ProductCreateSerializer
from sales_network.models import Factory, ContactInfo
from sales_network.serializers import ContactInfoBaseSerializer, MainNetworkBaseSerializer


class FactorySerializer(serializers.ModelSerializer):
    """
    Base Factory model serializer, with a broader info of the related objects (main_network, contact_info, products).
    """
    main_network = MainNetworkBaseSerializer(read_only=True)
    contact_info = ContactInfoBaseSerializer(read_only=True)
    products = ProductBaseSerializer(many=True, read_only=True)

    class Meta:
        model = Factory
        fields = ('id', 'main_network', 'name', 'contact_info', 'products', 'created_at', 'is_active')


class FactorySupplierSerializer(serializers.ModelSerializer):
    """
    A serializers for broader short supplier representation (id + name) used in related models' serializers.
    """
    class Meta:
        model = Factory
        fields = ('id', 'name',)


class FactoryCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for the Factory model objects creation.
    transaction.atomic() context is used in order to prevent any effects to the database,
    unless all the actions in the overridden create() method are successful.
    """
    contact_info = ContactInfoBaseSerializer(many=False, required=True)
    new_products = ProductCreateSerializer(many=True, required=False)
    product_ids_to_add = serializers.ListField(required=False)

    class Meta:
        model = Factory
        fields = ('id', 'name', 'main_network', 'contact_info', 'new_products', 'product_ids_to_add',)

    def create(self, validated_data):
        with transaction.atomic():
            contacts_data = validated_data.pop('contact_info')
            new_products_data = validated_data.pop('new_products', [])
            prod_ids_list = validated_data.pop('product_ids_to_add', [])

            contacts = ContactInfo.objects.create(**contacts_data)
            contacts.save()
            factory = Factory.objects.create(**validated_data, contact_info=contacts)

            for product in new_products_data:
                factory.products.create(**product)

            for prodict_id in prod_ids_list:
                try:
                    prod_to_add = get_object_or_404(Product, pk=prodict_id)
                    factory.products.add(prod_to_add)
                except Http404:
                    raise ValidationError(f'Product with "{prodict_id}" id not found')

            return factory


class FactoryUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for the Factory model objects update.
    transaction.atomic() context is used in order to prevent any effects to the database,
    unless all the actions in the overridden updated() method are successful.
    """
    name = serializers.CharField(required=False)
    contact_info_id = serializers.IntegerField(required=False)
    product_ids_to_add = serializers.ListField(child=serializers.IntegerField(), required=False)
    product_ids_to_remove = serializers.ListSerializer(child=serializers.IntegerField(), required=False)

    class Meta:
        model = Factory
        fields = (
            'id', 'name', 'contact_info_id', 'product_ids_to_add', 'product_ids_to_remove', 'is_active',
        )

    def update(self, factory, validated_data):
        with transaction.atomic():
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

            try:
                factory.save()
            except IntegrityError:
                raise serializers.ValidationError(
                    f'ContactInfo with "{contact_info_data}" id is already related to another entity.')
            return factory
