from django.db import models

from products.models import Product
from sales_network.models import ContactInfo, Factory, RetailNetwork
from sales_network.models.retail_network import NULLABLE


class SoleProprietor(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='proprietor_name')
    contact_info = models.OneToOneField(ContactInfo, on_delete=models.CASCADE, related_name='proprietor_contacts')
    products = models.ManyToManyField(Product, related_name='proprietor_products')
    factory_supplier = models.ForeignKey(Factory, on_delete=models.SET_NULL,
                                         verbose_name='proprietor_supplier',
                                         related_name='proprietor_supplier', **NULLABLE)
    retail_network_supplier = models.ForeignKey(RetailNetwork, on_delete=models.SET_NULL,
                                                verbose_name='proprietor_supplier',
                                                related_name='proprietor_supplier', **NULLABLE)
    debt_to_supplier = models.DecimalField(verbose_name='debt_to_supplier', decimal_places=2, max_digits=15)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
