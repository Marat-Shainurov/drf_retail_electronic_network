from rest_framework import generics

from sales_network.models import SoleProprietor
from sales_network.serializers import SoleProprietorSerializer, SoleProprietorCreateSerializer


class SoleProprietorCreateView(generics.CreateAPIView):
    serializer_class = SoleProprietorCreateSerializer


class SoleProprietorListView(generics.ListAPIView):
    serializer_class = SoleProprietorSerializer
    queryset = SoleProprietor.objects.all()
