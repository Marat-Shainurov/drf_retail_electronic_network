from django.db import models
from rest_framework.exceptions import ValidationError

from products.models import Product
from sales_network.models import ContactInfo, Factory, RetailNetwork, MainNetwork

NULLABLE = {'blank': True, 'null': True}


class SoleProprietor(models.Model):
    main_network = models.ForeignKey(MainNetwork, verbose_name='main_network', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, unique=True, verbose_name='proprietor_name')
    contact_info = models.OneToOneField(ContactInfo, on_delete=models.CASCADE, related_name='proprietor_contacts')
    products = models.ManyToManyField(Product, related_name='proprietor_products', blank=True)
    factory_supplier = models.ForeignKey(Factory, on_delete=models.SET_NULL,
                                         verbose_name='factory_supplier_for_proprietor',
                                         related_name='factory_supplier_for_proprietor', **NULLABLE)
    retail_network_supplier = models.ForeignKey(RetailNetwork, on_delete=models.SET_NULL,
                                                verbose_name='retail_network_supplier',
                                                related_name='retail_network_supplier', **NULLABLE)
    debt_to_supplier = models.DecimalField(verbose_name='debt_to_supplier', decimal_places=2, max_digits=15, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'"{self.name}" proprietor'

    class Meta:
        verbose_name = 'Sole Proprietor'
        verbose_name_plural = 'Sole Proprietors'

    def clean(self):
        if self.factory_supplier and self.retail_network_supplier:
            msg = "Sole Proprietor can have only one supplier (either factory_supplier or retail_network_supplier)."
            raise ValidationError(msg)

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.is_active = False
        self.contact_info.is_active = False
        self.contact_info.save()
        self.save()
