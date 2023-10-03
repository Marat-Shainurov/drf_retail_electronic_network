from django.db import models


class ContactInfo(models.Model):
    email = models.EmailField(verbose_name='entity_email')
    phone = models.CharField(max_length=20, verbose_name='entity_phone')
    country = models.CharField(max_length=100, verbose_name='entity_country')
    city = models.CharField(max_length=100, verbose_name='entity_city')
    street = models.CharField(max_length=100, verbose_name='entity_street')
    building = models.IntegerField(verbose_name='entity_building_number')
