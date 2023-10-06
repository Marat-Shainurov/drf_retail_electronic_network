from rest_framework import generics

from sales_network.models import SoleProprietor
from sales_network.serializers import SoleProprietorSerializer, SoleProprietorCreateSerializer, \
    SoleProprietorUpdateSerializer


class SoleProprietorCreateView(generics.CreateAPIView):
    serializer_class = SoleProprietorCreateSerializer


class SoleProprietorListView(generics.ListAPIView):
    serializer_class = SoleProprietorSerializer
    queryset = SoleProprietor.objects.all()


class SoleProprietorUpdateView(generics.UpdateAPIView):
    serializer_class = SoleProprietorUpdateSerializer
    queryset = SoleProprietor.objects.all()


class SoleProprietorRetrieveView(generics.RetrieveAPIView):
    serializer_class = SoleProprietorSerializer
    queryset = SoleProprietor.objects.all()


class SoleProprietorDeleteView(generics.DestroyAPIView):
    serializer_class = SoleProprietorSerializer
    queryset = SoleProprietor.objects.all()
