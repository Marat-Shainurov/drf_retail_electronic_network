from django.db import models


class Product(models.Model):
    name = models.CharField()
    product_model = models.CharField()
    launch_date = models.DateField()
    is_active = models.BooleanField(default=True)
