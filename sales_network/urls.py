from django.urls import path

from sales_network.apps import SalesNetworkConfig
from sales_network.views import (FactoryListAPIView, FactoryCreateAPIView, FactoryUpdateAPIView, FactoryRetrieveAPIView,
                                 FactoryDeleteAPIView, RetailNetCreateAPIView, RetailNetListAPIView,
                                 RetailNetRetrieveAPIView, RetailNetDeleteAPIView, RetailNetUpdateAPIView,
                                 SoleProprietorCreateView, SoleProprietorListView, SoleProprietorUpdateView,
                                 SoleProprietorRetrieveView, SoleProprietorDeleteView, MainNetCreateAPIView,
                                 MainNetListView, MainNetUpdateAPIView, MainNetRetrieveAPIView, MainNetDeleteAPIView)

app_name = SalesNetworkConfig.name

urlpatterns = [
    # main networks
    path("main-networks/", MainNetListView.as_view(), name='list_main_networks'),
    path("main-networks/create/", MainNetCreateAPIView.as_view(), name='create_main_networks'),
    path("main-networks/update/<int:pk>/", MainNetUpdateAPIView.as_view(), name='update_main_networks'),
    path("main-networks/get/<int:pk>/", MainNetRetrieveAPIView.as_view(), name='get_main_networks'),
    path("main-networks/delete/<int:pk>/", MainNetDeleteAPIView.as_view(), name='delete_main_networks'),

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
    path("retail-networks/update/<int:pk>/", RetailNetUpdateAPIView.as_view(), name='update_retail_network'),
    path("retail-networks/get/<int:pk>/", RetailNetRetrieveAPIView.as_view(),
         name='get_retail_network'),
    path("retail-networks/delete/<int:pk>/", RetailNetDeleteAPIView.as_view(), name='delete_retail_network'),

    # sole-proprietor
    path("sole-proprietors/", SoleProprietorListView.as_view(), name='list_sole_proprietor'),
    path("sole-proprietors/create/", SoleProprietorCreateView.as_view(), name='create_sole_proprietor'),
    path("sole-proprietors/update/<int:pk>/", SoleProprietorUpdateView.as_view(), name='update_sole_proprietor'),
    path("sole-proprietors/get/<int:pk>/", SoleProprietorRetrieveView.as_view(), name='get_sole_proprietor'),
    path("sole-proprietors/delete/<int:pk>/", SoleProprietorDeleteView.as_view(), name='delete_sole_proprietor'),
]
