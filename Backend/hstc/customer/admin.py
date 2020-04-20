from django.contrib import admin
from .models import Customer_Details, Customer, Inspection, Container_loading

from import_export.admin import ImportExportModelAdmin
# Register your models here.

# admin.site.register(Customer_Details)
# admin.site.register(Customer)
# admin.site.register(Inspection)
# admin.site.register(Container_loading)

@admin.register(Customer_Details, Customer, Inspection, Container_loading)
class ViewAdmin(ImportExportModelAdmin):
    pass