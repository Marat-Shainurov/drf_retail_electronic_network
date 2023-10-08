from django.db import models

from products.models import Product
from sales_network.models import ContactInfo, MainNetwork


class Factory(models.Model):
    main_network = models.ForeignKey(MainNetwork, verbose_name='main_network', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, unique=True, verbose_name='factory_name')
    contact_info = models.OneToOneField(ContactInfo, on_delete=models.CASCADE, related_name='factory_contacts')
    products = models.ManyToManyField(Product, related_name='factory_products', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'"{self.name}" factory'

    class Meta:
        verbose_name = 'Factory'
        verbose_name_plural = 'Factories'

    def delete(self, *args, **kwargs):
        self.is_active = False
        self.contact_info.is_active = False
        self.contact_info.save()
        self.save()
