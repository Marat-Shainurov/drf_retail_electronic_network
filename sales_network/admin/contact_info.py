from django.contrib import admin

from sales_network.models import ContactInfo


@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'phone', 'country', 'city', 'street', 'building',)
    list_filter = ('country', 'city', 'street',)
    search_fields = ('email', 'phone',)
