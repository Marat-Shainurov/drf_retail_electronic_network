from django.contrib import admin

from sales_network.models import Factory
from sales_network.services.filter_by_city import ContactInfoCityFilter


@admin.register(Factory)
class FactoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'contact_info', 'created_at', 'is_active',)
    list_filter = ('name', ContactInfoCityFilter, 'is_active',)
    search_fields = ('name',)
