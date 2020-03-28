from django import forms
from .models import Customer_Details, Customer

class customer_form(forms.ModelForm):
    class Meta:
        model=Customer_Details
        fields = '__all__'

class main_customer_form(forms.ModelForm):
    class Meta:
        model=Customer
        fields = '__all__'
