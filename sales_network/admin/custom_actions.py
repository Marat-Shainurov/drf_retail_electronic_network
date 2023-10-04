from django.contrib import admin


@admin.action(description="Assigns debt_to_supplier with 0.00.")
def clear_debt(model_admin, request, queryset):
    queryset.update(debt_to_supplier=0)
