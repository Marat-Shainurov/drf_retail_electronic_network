from django.contrib import admin

from sales_network.models import ContactInfo


@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'phone', 'country', 'city', 'street', 'building', 'is_active',)
    list_filter = ('country', 'city', 'is_active',)
    search_fields = ('email', 'phone',)
