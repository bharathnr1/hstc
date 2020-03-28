#Template Redirects
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect

#Importing Generic Views
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, FormView, UpdateView, DeleteView

#My Imports
from .forms import customer_form, main_customer_form
from .models import Customer_Details, Customer
from django.conf import settings

#Email Modules
from django.core.mail import send_mail, send_mass_mail
from django.core.mail import EmailMessage

#Excell Modules
import xlwt, os
from datetime import datetime

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
    
class Customer_Detail(DetailView):
    model = Customer_Details
    template_name='customer/customer_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class Customer_Update(UpdateView):
    model = Customer_Details
    fields = '__all__'

class Customer_Delete(DeleteView):
    model=Customer_Details
    success_url = reverse_lazy('customer:customer-list')

def send_CPI(request, pk):
    customer_object = get_object_or_404(Customer, pk=pk)
    vendor_object = Customer_Details.objects.filter(customer=customer_object).all()

    # """Creating Excell File for Customer PI and saving in Database then sending it across to customer and deleteing it from Database itself."""

    style0 = xlwt.easyxf('font: name Times New Roman, bold on')
    style1 = xlwt.easyxf(num_format_str='D-MMM-YY')
    style2 = xlwt.easyxf('font: name Times New Roman')

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


