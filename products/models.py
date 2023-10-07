from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='product_name', unique=True)
    product_model = models.CharField(max_length=50, verbose_name='product_model')
    launch_date = models.DateField(verbose_name='product_launch_date')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Config:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
