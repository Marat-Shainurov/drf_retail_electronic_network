from django.db import models

from products.models import Product
from sales_network.models import ContactInfo, Factory

NULLABLE = {'blank': True, 'null': True}


class RetailNetwork(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='network_name')
    contact_info = models.OneToOneField(ContactInfo, on_delete=models.CASCADE, related_name='network_contacts')
    products = models.ManyToManyField(Product, related_name='network_products')
    factory_supplier = models.ForeignKey(Factory, on_delete=models.SET_NULL,
                                         verbose_name='network_supplier', related_name='network_supplier', **NULLABLE)
    debt_to_supplier = models.DecimalField(verbose_name='debt_to_supplier', decimal_places=2, max_digits=15)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
