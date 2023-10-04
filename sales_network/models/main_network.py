from django.db import models

from products.models import Product
from sales_network.models import ContactInfo


class MainNetwork(models.Model):
    name = models.CharField(max_length=100, verbose_name='name', unique=True)
    contact_info = models.OneToOneField(ContactInfo, on_delete=models.CASCADE, related_name='main_network_contacts')
    products = models.ManyToManyField(Product, verbose_name='main_network_products', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Main Network'
        verbose_name_plural = 'Main Networks'
