from rest_framework import serializers

from sales_network.models import ContactInfo


class ContactInfoBaseSerializer(serializers.ModelSerializer):
    """
    Base ContactInfo serializer used by all the related models (contact_info field).
    """
    class Meta:
        model = ContactInfo
        fields = ('id', 'email', 'phone', 'country', 'city', 'street', 'building')
