from django.urls import path

from sales_network.apps import SalesNetworkConfig
from sales_network.views import (FactoryListAPIView, FactoryCreateAPIView, FactoryUpdateAPIView, FactoryRetrieveAPIView,
                                 FactoryDeleteAPIView)

app_name = SalesNetworkConfig.name

urlpatterns = [
    # factories
    path("suppliers/factories/", FactoryListAPIView.as_view(), name='list_factories'),
    path("suppliers/create-factory/", FactoryCreateAPIView.as_view(), name='create_factory'),
    path("suppliers/update-factory/<int:pk>/", FactoryUpdateAPIView.as_view(), name='update_factory'),
    path("suppliers/get-factory/<int:pk>/", FactoryRetrieveAPIView.as_view(), name='get_factory'),
    path("suppliers/delete-factory/<int:pk>/", FactoryDeleteAPIView.as_view(), name='delete_factory'),
    #
    # # retail-networks
    # path("suppliers/retail-networks/", RetailListAPIView.as_view(), name='list_retail_networks'),
    # path("suppliers/retail-networks/", RetailCreateAPIView.as_view(), name='create_retail_network'),
    # path("suppliers/update-retail-network/", RetailUpdateAPIView.as_view(), name='update_retail_network'),
    # path("suppliers/get-retail-network/", RetailRetrieveAPIView.as_view(), name='get_retail_network'),
    # path("suppliers/delete-retail-network/", RetailDeleteAPIView.as_view(), name='delete_retail_network'),
    #
    # # sole-proprietor
    # path("sole-proprietor/", RetailListAPIView.as_view(), name='list_retail_networks'),
    # path("create-sole-proprietor/", RetailCreateAPIView.as_view(), name='create_retail_network'),
    # path("update-sole-proprietor/", RetailUpdateAPIView.as_view(), name='update_retail_network'),
    # path("get-sole-proprietor/", RetailRetrieveAPIView.as_view(), name='get_retail_network'),
    # path("delete-sole-proprietor/", RetailDeleteAPIView.as_view(), name='delete_retail_network'),
]

# todo: finish all the endpoints
