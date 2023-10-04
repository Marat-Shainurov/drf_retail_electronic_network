from django.contrib import admin

from sales_network.models import RetailNetwork
from sales_network.admin import clear_debt
from sales_network.services.filter_by_city import ContactInfoCityFilter


@admin.register(RetailNetwork)
class RetailNetworkAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'contact_info', 'factory_supplier', 'debt_to_supplier', 'created_at', 'is_active'
    )
    list_filter = ('factory_supplier', ContactInfoCityFilter, 'is_active',)
    search_fields = ('name',)
    actions = [clear_debt]
