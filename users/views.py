from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from users.models import CustomUser
from users.permissions import IsUserActive
from users.serializers import CustomUserSerializer


class CustomUserViewSet(viewsets.ModelViewSet):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()
    permission_classes = [IsUserActive, IsAdminUser]
