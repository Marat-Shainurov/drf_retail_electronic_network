from django.contrib import admin

from sales_network.models import Factory, RetailNetwork, SoleProprietor, ContactInfo


@admin.register(Factory)
class FactoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'contact_info', 'created_at', 'is_active',)
    list_filter = ('name', 'is_active',)
    search_fields = ('name',)


@admin.register(RetailNetwork)
class RetailNetworkAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'contact_info', 'factory_supplier', 'debt_to_supplier', 'created_at', 'is_active'
    )
    list_filter = ('factory_supplier', 'is_active',)
    search_fields = ('name',)


@admin.register(SoleProprietor)
class SoleProprietorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'contact_info', 'factory_supplier', 'retail_network_supplier',
                    'debt_to_supplier', 'created_at', 'is_active',)
    list_filter = ('factory_supplier', 'retail_network_supplier', 'is_active',)
    search_fields = ('name',)


@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'phone', 'country', 'city', 'street', 'building',)
    list_filter = ('country', 'city', 'street',)
    search_fields = ('email', 'phone',)
