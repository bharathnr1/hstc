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
        widgets = {
            'customer_name': forms.TextInput(attrs={'class':'edit_cus'}), 
            }

class shipment_selection(forms.ModelForm):
    class Meta:
        model=Customer
        fields = ["shipment_type",]

class dilivery_selection(forms.ModelForm):
    class Meta:
        model=Customer
        fields = ["shipment_type",]

class oneshipment_form(forms.Form):
    dilivery_date = forms.DateField(label='Select the Delivery Date')


class partShipmentForm(forms.ModelForm):
    class Meta:
        model = Customer_Details
        fields = ("shipment_number",'manufacturing_days',)
        widgets = {
            'manufacturing_days': forms.TextInput(attrs={'class':'form-control'}),        
            'shipment_number': forms.TextInput(attrs={'class':'form-control'}),        
            }


