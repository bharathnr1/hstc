#Template Redirects
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect, HttpResponse

#Importing Generic Views
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, FormView, UpdateView, DeleteView

#My Imports
from .forms import customer_form, main_customer_form, shipment_selection, oneshipment_form, partShipmentForm, Inspection_Form, ContainerLoadingForm, UploadFileForm
from .models import Customer_Details, Customer, Inspection, Container_loading
from django.conf import settings

#Email Modules
from django.core.mail import send_mail, send_mass_mail
from django.core.mail import EmailMessage

#Python Modules
import xlwt, os, datetime, xlrd

#Retrieve Objects
from django.shortcuts import get_object_or_404

#PDF Modules
from io import BytesIO
from xhtml2pdf import pisa   
from django.template.loader import get_template 
from django.core.files.base import ContentFile

########################################################CUSTOMER########################################################

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

def main_Customer_Detail(request, pk):
    object = get_object_or_404(Customer, pk=pk)
    vendor_object = Customer_Details.objects.filter(customer=object).all()
    ss=shipment_selection()
    print("ss created and settings")
    if request.method == "POST":
        form = shipment_selection(request.POST)
        print("request confirmed")
        print(form.errors)
        if form.is_valid():
            print("forms valid")
            temp = form.save(commit=False)
            ix = Customer.objects.filter(id=pk)
            print(pk)
            ix.update(shipment_type=temp.shipment_type)
            print("Rendring to dilivery dates.")
            return HttpResponseRedirect(reverse('customer:dilivery_dates',args=[pk]))
    return render(request, "main_customer/main_customer_detail.html", {"vendor_list":vendor_object,"object":object, "form":ss})

def uplaod_file(request, pk):
# We need to check with bharath that is there any kind of dependancy on expand feature on customer detail page for expanding one vendor detail.
    object = get_object_or_404(Customer, pk=pk)
    form = UploadFileForm()
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            object.shipment_file = request.FILES['shipment_file']
            object.save()
            media_path = str(settings.MEDIA_ROOT).replace("\\","/")
            media_path = media_path.replace("/media", "")
            media_path = media_path + str(object.shipment_file.url)
            wb = xlrd.open_workbook(media_path)
            sheet = wb.sheet_by_index(0) 
#Below is for the format Validation
            if(     (sheet.cell_value(0 , 0)).lower().replace(' ', '') ==  "sno." 
                and (sheet.cell_value(0 , 1)).lower().replace(' ', '') ==  "listno." 
                and (sheet.cell_value(0 , 2)).lower().replace(' ', '') ==  "sub-listno." 
                and (sheet.cell_value(0 , 3)).lower().replace(' ', '') ==  "companyname" 
                and (sheet.cell_value(0 , 4)).lower().replace(' ', '') ==  "contactno." 
                and (sheet.cell_value(0 , 5)).lower().replace(' ', '') ==  "email" 
                and (sheet.cell_value(0 , 6)).lower().replace(' ', '') ==  "wechat" 
                and (sheet.cell_value(0 , 7)).lower().replace(' ', '') ==  "accountdetails"
                and (sheet.cell_value(0 , 8)).lower().replace(' ', '') ==  "invoicedate" 
                and (sheet.cell_value(0 , 9)).lower().replace(' ', '') ==  "invoiceno." 
                and (sheet.cell_value (0, 10)).lower().replace(' ', '') ==  "description" 
                and (sheet.cell_value (0, 11)).lower().replace(' ', '') ==  "model"  
                and (sheet.cell_value (0, 12)).lower().replace(' ', '') ==  "photo" 
                and (sheet.cell_value (0, 13)).lower().replace(' ', '') ==  "dimensions" 
                and (sheet.cell_value (0, 14)).lower().replace(' ', '') ==  "remarks" 
                and (sheet.cell_value (0, 15)).lower().replace(' ', '') ==  "unit" 
                and (sheet.cell_value (0, 16)).lower().replace(' ', '') ==  "unitprice" 
                and (sheet.cell_value (0, 17)).lower().replace(' ', '') ==  "qty"
                and (sheet.cell_value(0,18)).lower().replace(' ', '') == "customeramount" 
                and (sheet.cell_value(0,19)).lower().replace(' ', '') == "customeramountafterdiscount" 
                and (sheet.cell_value(0,20)).lower().replace(' ', '') == "commission%" 
                and (sheet.cell_value(0,21)).lower().replace(' ', '') == "commissionrmb" 
                and (sheet.cell_value(0,22)).lower().replace(' ', '') == "actualvendoramount" 
                and (sheet.cell_value(0,23)).lower().replace(' ', '') == "vendordeposit%" 
                and (sheet.cell_value(0,24)).lower().replace(' ', '') == "vendoradvancedepositamount" 
                and (sheet.cell_value(0,25)).lower().replace(' ', '') == "tokendeposit(customer)" 
                and (sheet.cell_value(0,26)).lower().replace(' ', '') == "tokendeposit(hstc)"
                and (sheet.cell_value(0,27)).lower().replace(' ', '') == "tokendepositdate"
                and (sheet.cell_value(0,28)).lower().replace(' ', '') == "vendoradvancebalance"
                and (sheet.cell_value(0,29)).lower().replace(' ', '') == "vendoradvancebalancepaid" 
                and (sheet.cell_value(0,30)).lower().replace(' ', '') == "advancebalancedate" 
                and (sheet.cell_value(0,31)).lower().replace(' ', '') == "vendorfinalbalance"
                and (sheet.cell_value(0,32)).lower().replace(' ', '') == "vendorfinalbalancedate" 
                and (sheet.cell_value(0,33)).lower().replace(' ', '') == "manufacturingdays"
                and (sheet.cell_value(0,34)).lower().replace(' ', '') == "plannedinspectiondate" 
                and (sheet.cell_value(0,35)).lower().replace(' ', '') == "actualinspectiondate" 
                and (sheet.cell_value(0,36)).lower().replace(' ', '') == "inspectiondoneby"
                and (sheet.cell_value(0,37)).lower().replace(' ', '') == "inspectionremarks" 
                and (sheet.cell_value(0,38)).lower().replace(' ', '') == "cbm(m3)" 
                and (sheet.cell_value(0,39)).lower().replace(' ', '') == "ctns" 
                and (sheet.cell_value(0,40)).lower().replace(' ', '') == "grossweight(kgs)" 
                and (sheet.cell_value(0,41)).lower().replace(' ', '') == "netweight(kgs)" ):
                print("Ready2")
#Below is for creating objects off the excell sheet
                for i in range(1, sheet.nrows):
                    print(True if type(sheet.cell_value(i , 1)) == type(1.0) else "Nope")
                    vendor_list = Customer_Details.objects.create( 
                                                                    customer = object,    
                                                                    s_no = int(sheet.cell_value(i , 0)) if type(sheet.cell_value(i , 0))  == type(1.0)  else None, 
                                                                    list_no     = int(sheet.cell_value(i , 1)) if type(sheet.cell_value(i , 1))  == type(1.0)  else None ,
                                                                    sub_list_no     = int(sheet.cell_value(i , 2)) if type(sheet.cell_value(i , 2))  == type(1.0)  else None ,
                                                                    company_name     = sheet.cell_value(i , 3) ,
                                                                    contact_no     = int(sheet.cell_value(i , 4)) if type(sheet.cell_value(i , 4)) == type(1.0) else None, 
                                                                    email     = sheet.cell_value(i , 5) if type(sheet.cell_value(i , 5))  == type(1.0)  else None, 
                                                                    wechat     = int(sheet.cell_value(i , 6)) if type(sheet.cell_value(i , 6))  == type(1.0)  else None, 
                                                                    account_details     = sheet.cell_value(i , 7),
                                                                    invoice_date     = datetime.datetime(*xlrd.xldate_as_tuple(sheet.cell_value(i,8), wb.datemode)) if type(sheet.cell_value(i , 8))  == type(1.0)  else None ,
                                                                    invoice_no     = int(sheet.cell_value(i , 9) ) if type(sheet.cell_value(i , 9))  == type(1.0)  else None, 
                                                                    description     = sheet.cell_value(i, 10),
                                                                    model     = sheet.cell_value(i, 11),
                                                                    photo     = sheet.cell_value(i, 12),
                                                                    dimensions     = sheet.cell_value(i, 13),
                                                                    remarks     = sheet.cell_value(i, 14) ,
                                                                    unit     = sheet.cell_value(i, 15),
                                                                    unit_price     = int(sheet.cell_value(i, 16)) if type(sheet.cell_value(i , 16)) == type(1.0)   else None, 
                                                                    qty     = int(sheet.cell_value(i, 17)) if type(sheet.cell_value(i , 17)) == type(1.0)   else None, 
                                                                    customer_amount     = int(sheet.cell_value(i,18)) if type(sheet.cell_value(i , 18)) == type(1.0)   else None, 
                                                                    customer_amount_after_discount     = int(sheet.cell_value(i,19)) if type(sheet.cell_value(i , 19))  == type(1.0)  else None, 
                                                                    commission_persentage     = sheet.cell_value(i,20),
                                                                    commission_rmb          = sheet.cell_value(i, 21),

                                                                    actual_vendor_amount    = int(sheet.cell_value(i,22)) if type(sheet.cell_value(i , 22))  == type(1.0)  else None,
                                                                    vendor_deposit_persentage    = int(sheet.cell_value(i,23)) if type(sheet.cell_value(i , 23))  == type(1.0)  else None,
                                                                    vendor_advance_deposit_amount    = int(sheet.cell_value(i,24)) if type(sheet.cell_value(i , 24))  == type(1.0)  else None,
                                                                    token_deposit_customer    = int(sheet.cell_value(i,25)) if type(sheet.cell_value(i , 25))  == type(1.0)  else None,
                                                                    token_deposit_HSTC    = int(sheet.cell_value(i,26)) if type(sheet.cell_value(i , 26))  == type(1.0)  else None,
                                                                    token_deposit_date    = datetime.datetime(*xlrd.xldate_as_tuple(sheet.cell_value(i,27), wb.datemode)) if type(sheet.cell_value(i , 27))  == type(1.0)  else None,
                                                                    vendor_advance_balance    = int(sheet.cell_value(i,28)) if type(sheet.cell_value(i , 28))  == type(1.0)  else None,
                                                                    vendor_advance_balance_paid    = int(sheet.cell_value(i,29)) if type(sheet.cell_value(i , 29))  == type(1.0)  else None,
                                                                    advance_balance_date    = datetime.datetime(*xlrd.xldate_as_tuple(sheet.cell_value(i,30), wb.datemode)) if type(sheet.cell_value(i , 30))  == type(1.0)  else None,
                                                                    vendor_final_balance    = int(sheet.cell_value(i,31)) if type(sheet.cell_value(i , 31))  == type(1.0)  else None,
                                                                    vendor_final_balance_date    = datetime.datetime(*xlrd.xldate_as_tuple(sheet.cell_value(i,32), wb.datemode) ) if type(sheet.cell_value(i , 32))  == type(1.0)  else None,
                                                                    manufacturing_days    = int(sheet.cell_value(i,33)) if type(sheet.cell_value(i , 33))  == type(1.0)  else None,
                                                                    CBM_m3    = int(sheet.cell_value(i,38)) if type(sheet.cell_value(i , 38))  == type(1.0)  else None,
                                                                    ctns    = int(sheet.cell_value(i,39)) if type(sheet.cell_value(i , 39))  == type(1.0)  else None,
                                                                    gross_weight_kgs    = int(sheet.cell_value(i,40)) if type(sheet.cell_value(i , 40))  == type(1.0)  else None,
                                                                    net_weight_kgs    = int(sheet.cell_value(i,41)) if type(sheet.cell_value(i , 41))  == type(1.0)  else None,
                                                                )
                    vendor_list.save()
                    print(type(sheet.cell_value(i,35)))
#Since we are setting up inspection while uploading the excell sheet, we need to setup a validation initially, and then crate the incpection model for which it doesnt exist.
                for i in range(1, sheet.nrows):
                    inspection_field = Inspection.objects.create(
                                                                customer = object,
                                                                vendor_company_name = get_object_or_404(Customer_Details, pk=vendor_list.pk),
                                                                actual_inspection_date = datetime.datetime(*xlrd.xldate_as_tuple(sheet.cell_value(i,35), wb.datemode)) if type(sheet.cell_value(i , 35))  == type(1.0)  else None,
                                                                inspection_done_by = sheet.cell_value(i,36),
                                                                inspection_remarks = sheet.cell_value(i,37),
                                                                planned_inspection_date = datetime.datetime(*xlrd.xldate_as_tuple(sheet.cell_value(i,34), wb.datemode)) if type(sheet.cell_value(i , 34))  == type(1.0)  else None,
                                                                )
                    inspection_field.save()
            else:
                return HttpResponse('The file format of uploaded file in not correct. Please use the excel format given as donwload in the portal.')       
        return HttpResponseRedirect(reverse('customer:main_customer-detail',args=[pk]))
    return render(request, 'main_customer/uploadfile.html', {"form":form})

class main_Customer_Update(UpdateView):
    model = Customer
    template_name='main_customer/main_customer_update_form.html'
    fields = '__all__'

class main_Customer_Delete(DeleteView):
    model=Customer
    template_name='main_customer/main_customer_details_confirm_delete.html'
    success_url = reverse_lazy('customer:main_customer-list')


########################################################Vendors CRUD one by one########################################################

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

########################################################CUSTOMER PI########################################################

def send_CPI(request, pk):
    customer_object = get_object_or_404(Customer, pk=pk)
    vendor_object = Customer_Details.objects.filter(customer=customer_object).all()
    """
    Creating Excell File for Customer PI and saving in Database then sending it across to customer and deleteing it from Database itself.

    """
# We need to find out a way to import the images in excel sheets. 
    style0 = xlwt.easyxf('font: name Times New Roman, bold on')
    style1 = xlwt.easyxf(num_format_str='D-MMM-YY')
    style2 = xlwt.easyxf('font: name Times New Roman')
    """ 
    Create field in model for saving customer PI File, for reupload, you wold need to delete the old file. 

    """
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
    """Email send to customer with created Customer PI"""
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

def shipment_type(request, pk):

    return render(request, 'dilivery/shipment_types.html')

########################################################DILIVERY DATES########################################################


def dilivery_dates(request, pk):
    customer_object = get_object_or_404(Customer, pk=pk)
    vendor_queryset = Customer_Details.objects.filter(customer=customer_object).all()
    y= partShipmentForm()

    inspection_obj = Inspection.objects.filter(customer=customer_object).all()
    print("Inspection data inside delivery function")
    print(inspection_obj)
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
        return render(request, "dilivery/DiliveryListView.html", {"vendor_queryset" : vendor_queryset, "partShipmentForm":y, "id":pk, "shipment": None, 'inspection_obj': inspection_obj})            

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

########################################################INSPECTIONS########################################################

def create_inspection(request, pk):
    customer_object = get_object_or_404(Customer, pk=pk)
    vendor_queryset = Customer_Details.objects.filter(customer=customer_object).all()
# Since we are setting up inspection on uploading the excell sheet, we need to setup a validation initially, and then crate the incpection model for which it doesnt exist.
    for i in vendor_queryset:
        inspection_field = Inspection.objects.create(
                                                    customer = customer_object,
                                                    vendor_company_name = i)
        inspection_field.save()
    return HttpResponseRedirect(reverse('customer:display_inspection',args=[pk]))

def display_inspection(request, pk):
    customer_object = get_object_or_404(Customer, pk=pk)
    inspection_obj = Inspection.objects.filter(customer=customer_object).all()

    inspection_form = Inspection_Form()
# this for auto uploading the data on inspection form - instance=inspection_obj / But we have multiobjects.
    Container_loading_obj = Container_loading.objects.filter(customer=customer_object).all()
    print("Inspection display: ")
    print(customer_object.id)
    return render(request, "inspection/inspection-details.html", {"inspection_obj":inspection_obj, "inspection_form":Inspection_Form, "id":pk, "Container_loading_obj": Container_loading_obj})
    

def update_inspection( request, pk, id):
    if request.method == "POST":
        form = Inspection_Form(request.POST, request.FILES)
        if form.is_valid():
            x=get_object_or_404(Inspection, pk=pk)
            if (form.cleaned_data["inspection_done_by"]):
                x.inspection_done_by = form.cleaned_data["inspection_done_by"]
            else:
                print("Else worked")

            if form.cleaned_data["inspection_remarks"]:
                x.inspection_remarks = form.cleaned_data["inspection_remarks"]
            else:
                pass

            if request.FILES.get('inspection_photo_1', False):
                x.inspection_photo_1 = request.FILES['inspection_photo_1']
            else:
                pass

            if request.FILES.get('inspection_photo_2', False):
                x.inspection_photo_2 = request.FILES['inspection_photo_2']
            else:
                pass

            if form.cleaned_data["actual_inspection_date"]:
                x.actual_inspection_date = form.cleaned_data["actual_inspection_date"]
            else:
                pass

            x.save()
    return HttpResponseRedirect(reverse('customer:display_inspection',args=[id]))

########################################################SHIPMENT MARKS########################################################


"""
Use to convert the image url to absolute URL 

"""
def link_callback(uri, rel):
    """
    Convert HTML URIs to absolute system paths so xhtml2pdf can access those
    resources

    """
    # use short variable names
    sUrl = settings.STATIC_URL      # Typically /static/
    sRoot = settings.STATIC_ROOT    # Typically /home/userX/project_static/
    mUrl = settings.MEDIA_URL       # Typically /static/media/
    mRoot = settings.MEDIA_ROOT     # Typically /home/userX/project_static/media/

    # convert URIs to absolute system paths
    if uri.startswith(mUrl):
        path = os.path.join(mRoot, uri.replace(mUrl, ""))
    elif uri.startswith(sUrl):
        path = os.path.join(sRoot, uri.replace(sUrl, ""))
    else:
        return uri  # handle absolute uri (ie: http://some.tld/foo.png)

    # make sure that file exists
    if not os.path.isfile(path):
            raise Exception(
                'media URI must start with %s or %s' % (sUrl, mUrl)
            )
    return path         
"""

1. We need to check while creating the Shipment marks how to lower down the resolution of the images that are being attachec
2. We need to create seprate button to send email to customer

"""

def getShipmentMarks(request, pk):
    customer_object = get_object_or_404(Customer, pk=pk)
    vendor_obj = Customer_Details.objects.filter(customer=customer_object).all()    
    data = {"vendor_obj":vendor_obj}
    template = get_template("get_shipmentMarks_pdf.html")
    html = template.render(data)
    response = BytesIO()
    x=str(settings.MEDIA_ROOT).replace("\\","/")
    x=x+"/mypdf.pdf"
    output = open(x, 'wb+')
    pdfPage = pisa.CreatePDF(html, dest=response, link_callback=link_callback)
    output.write(response.getvalue())
    output.close()
    email = EmailMessage(
            'Hello',
            'Body goes here',
            settings.EMAIL_HOST_USER,
            ["asisbagga@gmail.com"],
            ['asissingh.g@gmail.com'],
            headers={'Message-ID': 'foo'},)
    email.attach_file(x)
    email.send()
    os.remove(x)
    if not pdfPage.err:
       return HttpResponse(response.getvalue(), content_type="application/pdf")
    else:
        return HttpResponse("Oops got an Error, Try again!")

########################################################CONATINER LOADING########################################################


def create_cont_load(request, pk):
    customer_object = get_object_or_404(Customer, pk=pk)
    vendor_queryset = Customer_Details.objects.filter(customer=customer_object).all()
    for i in vendor_queryset:
        container_field = Container_loading.objects.create(
                                                    customer = customer_object,
                                                    vendor_company_name = i)
        container_field.save()
    return HttpResponseRedirect(reverse('customer:container_loading_list',args=[pk]))

def container_loading_list(request, pk):
    customer_object = get_object_or_404(Customer, pk=pk)
    Container_loading_obj = Container_loading.objects.filter(customer=customer_object).all()
    Container_loading_form = ContainerLoadingForm()
    return render(request, "container-loading/container-loading-details.html", { "Container_loading_obj":Container_loading_obj, "Container_loading_form":Container_loading_form, "id":pk })

def update_container_loading(request, pk, id):
    if request.method == "POST":
        form = ContainerLoadingForm(request.POST, request.FILES)
        if form.is_valid():
            x=get_object_or_404(Container_loading, pk=pk)
            if form.cleaned_data["PortDetails1"]:
                x.PortDetails1 = form.cleaned_data["PortDetails1"]
            else:
                pass

            if form.cleaned_data["PortDetails2"]:
                x.PortDetails2 = form.cleaned_data["PortDetails2"]
            else:
                pass

            if request.FILES.get('photo1', False):
                x.photo1 = request.FILES['photo1']
            else:
                print("didnt found anything")
                pass

            if request.FILES.get('photo2', False):
                x.photo2 = request.FILES['photo2']
            else:
                pass

            if request.FILES.get('photo3', False):
                x.photo3 = request.FILES['photo3']
            else:
                pass
            x.save()
    return HttpResponseRedirect(reverse('customer:container_loading_list',args=[id]))
