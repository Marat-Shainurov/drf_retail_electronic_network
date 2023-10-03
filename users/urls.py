from rest_framework.routers import DefaultRouter

from users.apps import UsersConfig
from users.views import CustomUserViewSet

app_name = UsersConfig.name

urlpatterns = []

router = DefaultRouter()
router.register(r'users', CustomUserViewSet, basename='users')
urlpatterns += router.urls
