from rest_framework import generics

from sales_network.models import Factory
from sales_network.serializers import FactorySerializer, FactoryCreateSerializer


class FactoryCreateAPIView(generics.CreateAPIView):
    serializer_class = FactoryCreateSerializer


class FactoryListAPIView(generics.ListAPIView):
    serializer_class = FactorySerializer
    queryset = Factory.objects.all()
