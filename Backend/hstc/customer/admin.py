from django.contrib import admin
from .models import Customer_Details, Customer, Inspection, Container_loading
# Register your models here.

admin.site.register(Customer_Details)
admin.site.register(Customer)
admin.site.register(Inspection)
admin.site.register(Container_loading)
