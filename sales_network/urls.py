from django.urls import path

from sales_network.apps import SalesNetworkConfig
from sales_network.views import (FactoryListAPIView, FactoryCreateAPIView, FactoryUpdateAPIView, FactoryRetrieveAPIView,
                                 FactoryDeleteAPIView, RetailNetCreateAPIView, RetailNetListAPIView,
                                 RetailNetRetrieveAPIView, RetailNetDeleteAPIView, RetailNetUpdateAPIView)

app_name = SalesNetworkConfig.name

urlpatterns = [
    # factories
    path("factories/", FactoryListAPIView.as_view(), name='list_factories'),
    path("factories/create/", FactoryCreateAPIView.as_view(), name='create_factory'),
    path("factories/update/<int:pk>/", FactoryUpdateAPIView.as_view(), name='update_factory'),
    path("factories/get/<int:pk>/", FactoryRetrieveAPIView.as_view(), name='get_factory'),
    path("factories/delete/<int:pk>/", FactoryDeleteAPIView.as_view(), name='delete_factory'),

    # retail-networks
    path("retail-networks/", RetailNetListAPIView.as_view(), name='list_retail_networks'),
    path("retail-networks/create/", RetailNetCreateAPIView.as_view(),
         name='create_retail_network'),
    path("retail-networks/update/<int:pk>", RetailNetUpdateAPIView.as_view(), name='update_retail_network'),
    path("retail-networks/get/<int:pk>", RetailNetRetrieveAPIView.as_view(),
         name='get_retail_network'),
    path("retail-networks/delete/<int:pk>", RetailNetDeleteAPIView.as_view(), name='delete_retail_network'),

    # # sole-proprietor
    # path("sole-proprietor/", RetailListAPIView.as_view(), name='list_retail_networks'),
    # path("create-sole-proprietor/", RetailCreateAPIView.as_view(), name='create_retail_network'),
    # path("update-sole-proprietor/", RetailUpdateAPIView.as_view(), name='update_retail_network'),
    # path("get-sole-proprietor/", RetailRetrieveAPIView.as_view(), name='get_retail_network'),
    # path("delete-sole-proprietor/", RetailDeleteAPIView.as_view(), name='delete_retail_network'),
]

# todo: finish all the endpoints
