from rest_framework import serializers

from sales_network.models import ContactInfo


class ContactInfoBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactInfo
        fields = ('id', 'email', 'phone', 'country', 'city', 'street', 'building')
