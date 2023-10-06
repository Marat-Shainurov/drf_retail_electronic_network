from rest_framework import generics

from sales_network.models import SoleProprietor
from sales_network.serializers import SoleProprietorSerializer, SoleProprietorCreateSerializer, \
    SoleProprietorUpdateSerializer
from users.permissions import IsUserActive


class SoleProprietorCreateView(generics.CreateAPIView):
    serializer_class = SoleProprietorCreateSerializer
    permission_classes = [IsUserActive]


class SoleProprietorListView(generics.ListAPIView):
    serializer_class = SoleProprietorSerializer
    queryset = SoleProprietor.objects.all()
    permission_classes = [IsUserActive]


class SoleProprietorUpdateView(generics.UpdateAPIView):
    serializer_class = SoleProprietorUpdateSerializer
    queryset = SoleProprietor.objects.all()
    permission_classes = [IsUserActive]


class SoleProprietorRetrieveView(generics.RetrieveAPIView):
    serializer_class = SoleProprietorSerializer
    queryset = SoleProprietor.objects.all()
    permission_classes = [IsUserActive]


class SoleProprietorDeleteView(generics.DestroyAPIView):
    serializer_class = SoleProprietorSerializer
    queryset = SoleProprietor.objects.all()
    permission_classes = [IsUserActive]
