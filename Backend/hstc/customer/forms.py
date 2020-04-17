from django import forms
from .models import Customer_Details, Customer, Inspection, Container_loading
from django.utils.translation import gettext_lazy as _


# CUSTOMER FORMS
class customer_form(forms.ModelForm):
    class Meta:
        model=Customer_Details
        fields = '__all__'

class main_customer_form(forms.ModelForm):
    class Meta:
        model=Customer
        fields = '__all__'

# Dilivery Dates FORMS

class shipment_selection(forms.ModelForm):
    class Meta:
        model=Customer
        fields = ["shipment_type",]

class dilivery_selection(forms.ModelForm):
    class Meta:
        model=Customer
        fields = ["shipment_type",]

class oneshipment_form(forms.Form):
    dilivery_date = forms.DateField(label='Select the Dilivery Date')

class partShipmentForm(forms.ModelForm):
    class Meta:
        model = Customer_Details
        fields = ("shipment_number",
                  'manufacturing_days',)
        widgets = {
            'manufacturing_days': forms.TextInput(attrs={'class':'form-control'}),        
            'shipment_number': forms.TextInput(attrs={'class':'form-control'}),        
            }

# Inspection FORMS

class Inspection_Form(forms.ModelForm):
    class Meta:
        model = Inspection
        fields = ("inspection_done_by",
                  "inspection_remarks",
                  "inspection_photo_1",
                  "inspection_photo_2",
                  "actual_inspection_date")
        labels = {
        'inspection_done_by': _('Inspector Name'),
        'inspection_remarks': _('Inspector Remarks'),
        'inspection_photo_1': _('Upload Inspection Image 1'),
        'inspection_photo_2': _('Upload Inspection Image 2'),
        'actual_inspection_date': _('Actual Visit Date'),        
        }
        widgets = {
            'inspection_done_by': forms.TextInput(attrs={'class':'form-control'}),        
            'inspection_remarks': forms.TextInput(attrs={'class':'form-control'}),                
            'actual_inspection_date': forms.TextInput(attrs={'class':'form-control'}),        
            }
        
# CONTAINER LOADING FORMS

class ContainerLoadingForm(forms.ModelForm):
    class Meta:
        model = Container_loading
        fields = (
            'photo1',
            'photo2',
            'photo3',
            'PortDetails1',
            'PortDetails2',
        )
        widgets = {
            'PortDetails1': forms.TextInput(attrs={'class':'form-control'}),                
            'PortDetails2': forms.TextInput(attrs={'class':'form-control'}),        
            }