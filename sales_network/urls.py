from django.urls import path

from sales_network.apps import SalesNetworkConfig
from sales_network.views.factory import FactoryListAPIView, FactoryCreateAPIView

app_name = SalesNetworkConfig.name

urlpatterns = [
    path("suppliers/factories/", FactoryListAPIView.as_view(), name='list_factories'),
    path("suppliers/create-factory/", FactoryCreateAPIView.as_view(), name='create_factory'),
]
