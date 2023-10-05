from rest_framework import generics

from sales_network.models import RetailNetwork
from sales_network.serializers import RetailNetSerializer, RetailNetCreateSerializer, RetailNetUpdateSerializer


class RetailNetCreateAPIView(generics.CreateAPIView):
    serializer_class = RetailNetCreateSerializer


class RetailNetListAPIView(generics.ListAPIView):
    serializer_class = RetailNetSerializer
    queryset = RetailNetwork.objects.all()


class RetailNetRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = RetailNetSerializer
    queryset = RetailNetwork.objects.all()


class RetailNetUpdateAPIView(generics.UpdateAPIView):
    serializer_class = RetailNetUpdateSerializer
    queryset = RetailNetwork.objects.all()


class RetailNetDeleteAPIView(generics.DestroyAPIView):
    serializer_class = RetailNetSerializer
    queryset = RetailNetwork.objects.all()
