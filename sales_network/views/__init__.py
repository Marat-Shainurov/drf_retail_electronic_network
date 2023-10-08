from .main_network import MainNetCreateAPIView, MainNetListView, MainNetUpdateAPIView, MainNetRetrieveAPIView, \
    MainNetDeleteAPIView
from .factory import FactoryCreateAPIView, FactoryListAPIView, FactoryUpdateAPIView, FactoryRetrieveAPIView, \
    FactoryDeleteAPIView
from .retail_network import RetailNetCreateAPIView, RetailNetListAPIView, RetailNetRetrieveAPIView, \
    RetailNetDeleteAPIView, RetailNetUpdateAPIView
from .sole_proprietor import SoleProprietorCreateView, SoleProprietorListView, SoleProprietorUpdateView, \
    SoleProprietorRetrieveView, SoleProprietorDeleteView

__all__ = [
    'MainNetCreateAPIView', 'MainNetListView', 'MainNetUpdateAPIView', 'MainNetRetrieveAPIView', 'MainNetDeleteAPIView',
    'FactoryCreateAPIView', 'FactoryListAPIView', 'FactoryUpdateAPIView', 'FactoryRetrieveAPIView',
    'FactoryDeleteAPIView',
    'RetailNetCreateAPIView', 'RetailNetListAPIView', 'RetailNetRetrieveAPIView', 'RetailNetDeleteAPIView',
    'RetailNetUpdateAPIView',
    'SoleProprietorCreateView', 'SoleProprietorListView', 'SoleProprietorUpdateView', 'SoleProprietorRetrieveView',
    'SoleProprietorDeleteView',
]
