from django.db import models

from products.models import Product
from sales_network.models import ContactInfo


class Factory(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='factory_name')
    contact_info = models.OneToOneField(ContactInfo, on_delete=models.CASCADE, related_name='factory_contacts')
    products = models.ManyToManyField(Product, related_name='factory_products')
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
