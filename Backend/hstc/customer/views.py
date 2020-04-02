#Template Redirects
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect

#Importing Generic Views
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, FormView, UpdateView, DeleteView

#My Imports
from .forms import customer_form, main_customer_form, shipment_selection, oneshipment_form, partShipmentForm
from .models import Customer_Details, Customer
from django.conf import settings

#Email Modules
from django.core.mail import send_mail, send_mass_mail
from django.core.mail import EmailMessage

#Python Modules
import xlwt, os, datetime

#Retrieve Objects
from django.shortcuts import get_object_or_404

#CUSTOMER CRUD APPS

def main_Customer_Create(request):
    info_form=main_customer_form()
    if request.method == "POST":
        print("Got Request")
        form = main_customer_form(request.POST)
        print(form.errors) 
        if form.is_valid():
            print("Form is Valid")
            temp = form.save(commit=False)
            temp.save()
            print("Form is Saved and you are redirected to list page")
            return HttpResponseRedirect(reverse('customer:main_customer-list'))
    return render(request, "main_customer/main_customer_details_form.html", {"form":info_form})


class main_Customer_List(ListView):
    model = Customer
    template_name='main_customer/main_customer_list.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class main_Customer_Detail(DetailView):
    model = Customer
    template_name='main_customer/main_customer_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        """" The queryset is filtered as per the customer object, 
        if there is two object for the same customer then we need to make sure
        the older is object is coming with a value hence we need to add
        avoid_duplication as a integer value and same value should be 
        stored in Customer object as a reffernce of comparision, maybe we can store customer_details pk value as integer in customer
        As of now i am going with assumption that there is only one customer"""
        context["vendor_list"] = Customer_Details.objects.filter(customer=self.object).all()
        return context

class main_Customer_Update(UpdateView):
    model = Customer
    template_name='main_customer/main_customer_update_form.html'
    fields = '__all__'

class main_Customer_Delete(DeleteView):
    model=Customer
    template_name='main_customer/main_customer_details_confirm_delete.html'
    success_url = reverse_lazy('customer:main_customer-list')


#Vendor CRUD Applications

def Customer_Create(request, pk):
    info_form=customer_form()
    if request.method == "POST":
        print("Got Request")
        form = customer_form(request.POST,request.FILES)
        print(form.errors) 
        if form.is_valid():
            print("Form is Valid")
            temp = form.save(commit=False)
            temp.customer = get_object_or_404(Customer, pk=pk)
            temp.save()
            print("Form is Saved and you are redirected to list page")
            return HttpResponseRedirect(reverse('customer:main_customer-detail', args=[pk]))
    return render(request, "customer/customer_details_form.html", {"form":info_form})
""" UPload and download button for Excell Sheets needs to be added. 
    Change form for creation
    put formulae for fields
"""
    
def customer_pi_list(request, pk):
    customer_object = get_object_or_404(Customer, pk=pk)
    vendor_object = Customer_Details.objects.filter(customer=customer_object).all()
    return render(request, "customer_PI/customer_pi_list.html", {"customer_object":customer_object, "vendor_object":vendor_object})


class Customer_Update(UpdateView):
    model = Customer_Details
    fields = '__all__'

class Customer_Delete(DeleteView):
    model=Customer_Details
    success_url = reverse_lazy('customer:main_customer-list')

def send_CPI(request, pk):
    customer_object = get_object_or_404(Customer, pk=pk)
    vendor_object = Customer_Details.objects.filter(customer=customer_object).all()

    # """Creating Excell File for Customer PI and saving in Database then sending it across to customer and deleteing it from Database itself."""

    style0 = xlwt.easyxf('font: name Times New Roman, bold on')
    style1 = xlwt.easyxf(num_format_str='D-MMM-YY')
    style2 = xlwt.easyxf('font: name Times New Roman')
    """ Create field in model for saving customer PI File, for reupload, you wold need to delete the old file. """
    wb = xlwt.Workbook()
    ws = wb.add_sheet('PI LIST')
    ws.write(0, 0,  "S No.",   style0)
    ws.write(0, 1,  "List No.",   style0)
    ws.write(0, 2,  "Sub-List No.",   style0)
    ws.write(0, 3,  "Discription",   style0)
    ws.write(0, 4,  "Model",   style0)
    ws.write(0, 5,  "Photo",   style0)
    ws.write(0, 6,  "Dimension",   style0)
    ws.write(0, 7,  "Remarks",   style0)
    ws.write(0, 8,  "Unit",   style0)
    ws.write(0, 9,  "Unit Price",   style0)
    ws.write(0, 10, "Qty",   style0)
    ws.write(0, 11, "Amount",   style0)
    ws.write(0, 12, "Amount After Discount",   style0)
    ws.write(0, 13, "Token Deposit by you",   style0)
    ws.write(0, 14, "Token Deposit by HSTC",   style0)
    ws.write(0, 15, "Token Deposit Date",   style0)
    ws.write(0, 16,  "CBM(m3)",   style0)
    ws.write(0, 17,  "Ctns",   style0)
    ws.write(0, 18,  "Gross Weight",   style0)
    ws.write(0, 19,  "Net Weight",   style0)
    dummy=1
    for i in vendor_object:
        ws.write(dummy, 0,  i.s_no ,   style2)
        ws.write(dummy, 1,  i.list_no ,   style2)
        ws.write(dummy, 2,  i.sub_list_no ,   style2)
        ws.write(dummy, 3,  i.description ,   style2)
        ws.write(dummy, 4,  i.model ,   style2)
        # ws.write(dummy, 5,  i.photo ,   style2)
        #removing photo because its not yet sorted!
        ws.write(dummy, 6,  i.dimensions ,   style2)
        ws.write(dummy, 7,  i.remarks ,   style2)
        ws.write(dummy, 8,  i.unit ,   style2)
        ws.write(dummy, 9,  i.unit_price ,   style2)
        ws.write(dummy, 10,  i.qty ,   style2)
        ws.write(dummy, 11,  i.customer_amount ,   style2)
        ws.write(dummy, 12,  i.customer_amount_after_discount ,   style2)
        ws.write(dummy, 13,  i.token_deposit_customer ,   style2)
        ws.write(dummy, 14,  i.token_deposit_HSTC ,   style2)
        ws.write(dummy, 15,  i.token_deposit_date ,   style1)
        ws.write(dummy, 16,  i.CBM_m3 ,   style2)
        ws.write(dummy, 17,  i.ctns ,   style2)
        ws.write(dummy, 18,  i.gross_weight_kgs ,   style2)
        ws.write(dummy, 19,  i.net_weight_kgs ,   style2)
        dummy=dummy+1
    x=str(settings.MEDIA_ROOT).replace("\\","/")
    wb.save(x + '/CustomerPI.xls')

    x=x + '/CustomerPI.xls'    
    #Email send to customer with created Customer PI
    email = EmailMessage(
    'Hello',
    'Body goes here',
    settings.EMAIL_HOST_USER,
    ["asisbagga@gmail.com"],
    ['asissingh.g@gmail.com'],
    headers={'Message-ID': 'foo'},
    )
    email.attach_file(x)
    email.send()
    os.remove(x)
    return HttpResponseRedirect(reverse('customer:main_customer-detail', args=[pk]))

class CustomerPI_Update(UpdateView):
    model = Customer_Details
    fields = ['s_no',
            'list_no',
            'sub_list_no',
            'description',
            'model',
            'photo',
            'dimensions',
            'remarks',
            'unit',
            'unit_price',
            'qty',
            'customer_amount',
            'customer_amount_after_discount',
            'token_deposit_customer',
            'token_deposit_HSTC',
            'token_deposit_date',
            'CBM_m3',
            'ctns',
            'gross_weight_kgs',
            'net_weight_kgs',]
    template_name = 'customer_PI/Customer_PI_details_form.html'
# Customer PI Requirements: 
# 1. Create Customer PI forms
# 2. Create a View for Customer PI
# 3. provide Edit, Delete Buttons for it

# small form of customer
# customer created
# uploading vendor sheet excell button
# exctract Customer PI required data and display it in customer Details page
# Verfiy and send email customer PI.
# If supose any changes is required the add, edit and delete will be there.
# They will make changes will be done on excell sheet, so there will be re upload button for same thing. 
# for reupload old object is deleted and will create another then same thing send PI Buton and Send Contract Email Button 

def shipment_type(request, pk):
    ss=shipment_selection()
    print("ss created and settings")
    if request.method == "POST":
        form = shipment_selection(request.POST)
        print("request confirmed")
        print(form.errors)
        if form.is_valid():
            print("forms valid")
            temp = form.save(commit=False)
            ix=Customer.objects.filter(id=pk)
            print(pk)
            ix.update(shipment_type=temp.shipment_type)
            print("Rendring to dilivery dates.")
            return HttpResponseRedirect(reverse('customer:dilivery_dates',args=[pk]))
    return render(request, 'dilivery/shipment_types.html', {"form":ss})

def dilivery_dates(request, pk):
    customer_object = get_object_or_404(Customer, pk=pk)
    vendor_queryset = Customer_Details.objects.filter(customer=customer_object).all()
    y= partShipmentForm()
    if customer_object.shipment_type == "One Shipment":
        x=oneshipment_form()
        if request.method == "POST":
            post_form = oneshipment_form(request.POST)
            if post_form.is_valid():
                dates = post_form.cleaned_data["dilivery_date"]
                for i in vendor_queryset:
                    i.tentative_dilivery_date= dates
                    i.planned_inspection_date=( dates - datetime.timedelta(days=3))
                    i.shipment_number=1
                    i.save()
                return render(request, "dilivery/DiliveryListView.html", {"vendor_queryset":vendor_queryset, "partShipmentForm":x,"id":pk, "shipment":customer_object.shipment_type})        
        return render(request, "dilivery/oneshipment.html", { "x":x })
    elif customer_object.shipment_type == "Part Shipments":
        return render(request, "dilivery/DiliveryListView.html", {"vendor_queryset" : vendor_queryset, "partShipmentForm":y, "id":pk, "shipment": None})            

def updatedates(request, pk, id):
    print("ID: ",id)
    print("/n PK: ", pk)
    print(request.POST.get('previous_page'))
    if request.method=="POST":
        form = partShipmentForm(request.POST)
        if form.is_valid():
            x=get_object_or_404(Customer_Details, pk=pk)
            tent_date= x.advance_balance_date + datetime.timedelta(days=form.cleaned_data["manufacturing_days"])
            print(tent_date)
            x.planned_inspection_date = tent_date -  datetime.timedelta(days=3)
            print(x.planned_inspection_date)
            x.shipment_number=form.cleaned_data["shipment_number"]
            x.manufacturing_days=form.cleaned_data["manufacturing_days"]
            x.tentative_dilivery_date = tent_date
            print(x.tentative_dilivery_date)
            x.save()
    return HttpResponseRedirect(reverse('customer:dilivery_dates',args=[id]))
