from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics

from sales_network.models import Factory
from sales_network.serializers import FactorySerializer, FactoryCreateSerializer, FactoryUpdateSerializer
from users.permissions import IsUserActive


class FactoryCreateAPIView(generics.CreateAPIView):
    serializer_class = FactoryCreateSerializer


class FactoryListAPIView(generics.ListAPIView):
    serializer_class = FactorySerializer
    queryset = Factory.objects.all()
    permission_classes = [IsUserActive]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['contact_info__city', ]


class FactoryUpdateAPIView(generics.UpdateAPIView):
    serializer_class = FactoryUpdateSerializer
    queryset = Factory.objects.all()
    permission_classes = [IsUserActive]


class FactoryRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = FactorySerializer
    queryset = Factory.objects.all()
    permission_classes = [IsUserActive]


class FactoryDeleteAPIView(generics.DestroyAPIView):
    serializer_class = FactorySerializer
    queryset = Factory.objects.all()
    permission_classes = [IsUserActive]
