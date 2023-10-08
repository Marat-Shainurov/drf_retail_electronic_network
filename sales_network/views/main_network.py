from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics

from sales_network.models import MainNetwork
from sales_network.pagination import BaseNetworkPagination
from sales_network.serializers import MainNetworkSerializer, MainNetworkCreateSerializer, MainNetworkUpdateSerializer
from users.permissions import IsUserActive


class MainNetCreateAPIView(generics.CreateAPIView):
    serializer_class = MainNetworkCreateSerializer
    queryset = MainNetwork.objects.all()
    permission_classes = [IsUserActive]


class MainNetListView(generics.ListAPIView):
    serializer_class = MainNetworkSerializer
    queryset = MainNetwork.objects.all()
    permission_classes = [IsUserActive]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['contact_info__city', ]
    pagination_class = BaseNetworkPagination


class MainNetUpdateAPIView(generics.UpdateAPIView):
    serializer_class = MainNetworkUpdateSerializer
    queryset = MainNetwork.objects.all()
    permission_classes = [IsUserActive]


class MainNetRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = MainNetworkSerializer
    queryset = MainNetwork.objects.all()
    permission_classes = [IsUserActive]


class MainNetDeleteAPIView(generics.DestroyAPIView):
    serializer_class = MainNetworkSerializer
    queryset = MainNetwork.objects.all()
    permission_classes = [IsUserActive]
