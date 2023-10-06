from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics

from sales_network.models import RetailNetwork
from sales_network.serializers import RetailNetSerializer, RetailNetCreateSerializer, RetailNetUpdateSerializer
from users.permissions import IsUserActive


class RetailNetCreateAPIView(generics.CreateAPIView):
    serializer_class = RetailNetCreateSerializer
    permission_classes = [IsUserActive]


class RetailNetListAPIView(generics.ListAPIView):
    serializer_class = RetailNetSerializer
    queryset = RetailNetwork.objects.all()
    permission_classes = [IsUserActive]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['contact_info__city', ]


class RetailNetRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = RetailNetSerializer
    queryset = RetailNetwork.objects.all()
    permission_classes = [IsUserActive]


class RetailNetUpdateAPIView(generics.UpdateAPIView):
    serializer_class = RetailNetUpdateSerializer
    queryset = RetailNetwork.objects.all()
    permission_classes = [IsUserActive]


class RetailNetDeleteAPIView(generics.DestroyAPIView):
    serializer_class = RetailNetSerializer
    queryset = RetailNetwork.objects.all()
    permission_classes = [IsUserActive]
