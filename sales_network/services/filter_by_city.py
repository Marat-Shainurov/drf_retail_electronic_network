from django.contrib import admin

from sales_network.models import ContactInfo


class ContactInfoCityFilter(admin.SimpleListFilter):
    """
    Custom filter class for the admin interface.
    Filters objects by their contact_info__city,
    based on the One-To-One relation with the ContactInfo model.
    """
    title = 'City'
    parameter_name = 'contact_info__city'

    def lookups(self, request, model_admin):
        cities = ContactInfo.objects.values_list('city', flat=True).distinct()
        return [(city, city) for city in cities]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(contact_info__city=self.value())
        return queryset
