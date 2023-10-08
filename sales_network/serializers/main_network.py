from rest_framework import serializers

from sales_network.models import MainNetwork


class MainNetworkBaseSerializer(serializers.ModelSerializer):
    """
    Base MainNetwork serializer used in all the related models serializers.
    """
    class Meta:
        model = MainNetwork
        fields = ('id', 'name',)
