from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy, reverse
from django.shortcuts import get_object_or_404

from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, FormView, UpdateView, DeleteView

from .forms import customer_form, main_customer_form
from .models import Customer_Details, Customer

from django.http import HttpResponseRedirect


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
