from rest_framework import serializers

from sales_network.models import MainNetwork


class MainNetworkBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainNetwork
        fields = ('id', 'name',)
