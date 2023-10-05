from rest_framework import generics

from sales_network.models import Factory
from sales_network.serializers import FactorySerializer, FactoryCreateSerializer, FactoryUpdateSerializer


class FactoryCreateAPIView(generics.CreateAPIView):
    serializer_class = FactoryCreateSerializer


class FactoryListAPIView(generics.ListAPIView):
    serializer_class = FactorySerializer
    queryset = Factory.objects.all()


class FactoryUpdateAPIView(generics.UpdateAPIView):
    serializer_class = FactoryUpdateSerializer
    queryset = Factory.objects.all()


class FactoryRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = FactorySerializer
    queryset = Factory.objects.all()


class FactoryDeleteAPIView(generics.DestroyAPIView):
    serializer_class = FactorySerializer
    queryset = Factory.objects.all()
