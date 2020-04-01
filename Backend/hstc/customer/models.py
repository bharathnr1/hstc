from django.db import models

# Create your models here.

ENTRY_CHOICES = (
    ('One Shipment','One Shipment'),
    ('Part Shipments','Part Shipments'),
)


class Customer(models.Model):
    customer_name = models.CharField(max_length=30)
    customer_contact = models.IntegerField()
    customer_email = models.EmailField()
    customer_company = models.CharField(max_length=100)
    shipment_type = models.CharField(max_length=50, choices=ENTRY_CHOICES, blank=True)

    def __str__(self):
        return self.customer_name

    def get_absolute_url(self):
        x=self.pk
        return f'/customer/main_customer-details/{x}'


class Customer_Details(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    """ Customer Details """
    s_no = 	models.IntegerField()
    list_no = models.IntegerField()
    sub_list_no =models.IntegerField()
    company_name= models.CharField(max_length=100)
    contact_no=models.IntegerField()
    email =models.EmailField()
    wechat =models.IntegerField()
    invoice_date =models.DateField()
    invoice_no =models.IntegerField()
    description =models.CharField(max_length=200)
    model =models.CharField(max_length=100)
    photo =models.ImageField()
    dimensions =models.CharField(max_length=100)
    remarks =models.CharField(max_length=200)
    unit =models.CharField(max_length=100)
    unit_price =models.IntegerField()
    qty=models.IntegerField()
    customer_amount =models.IntegerField()
    customer_amount_after_discount =models.IntegerField()
    commission =models.IntegerField()
    actual_vendor_amount =models.IntegerField()
    vendor_deposit_persentage= models.IntegerField()
    vendor_advance_deposit_amount =models.IntegerField()
    token_deposit_customer =models.IntegerField()
    token_deposit_HSTC =models.IntegerField()
    token_deposit_date =models.DateField()
    vendor_advance_balance =models.IntegerField()
    vendor_advance_balance_paid =models.IntegerField()
    advance_balance_date =models.DateField()
    vendor_final_balance =models.IntegerField()
    vendor_final_balance_date =models.DateField()
    account_details =models.CharField(max_length=200)
    manufacturing_days =models.IntegerField()

    CBM_m3 =models.IntegerField()
    ctns =models.IntegerField()
    gross_weight_kgs =models.IntegerField()
    net_weight_kgs =models.IntegerField()

    shipment_number = models.IntegerField()
    tentative_dilivery_date = models.DateField()
    planned_inspection_date = models.DateField()
 
    def __str__(self):
        return "Vendor: " + self.company_name
    
    def get_absolute_url(self):
        x=self.customer.pk
        return f'/customer/main_customer-details/{x}'


class Inspection(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    vendor_company_name = models.ForeignKey(Customer_Details, on_delete=models.CASCADE)
    "INSPECTION DETAILS"
   
    actual_inspection_date = models.DateField()
    inspection_done_by  = models.CharField(max_length=300)
    inspection_remarks = models.CharField(max_length=300)

    inspection_photo_1 = models.ImageField()
    inspection_photo_2 = models.ImageField()

    def __str__(self):
        return "INSPECTION for: " + self.customer + "on vendor: " + self.vendor_company_name


"""" Remove Customer PI in model, create form for edits, and hide  """
class Customer_PI(models.Model):

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    s_no = models.IntegerField()
    list_no = models.IntegerField()
    sub_list_no = models.IntegerField()
    description = models.CharField(max_length=200)
    model = models.CharField(max_length=100)
    photo = models.ImageField()
    dimensions = models.CharField(max_length=100)
    remarks = models.CharField(max_length=200)
    unit = models.CharField(max_length=100)
    unit_Price = models.IntegerField()
    qty = models.IntegerField()
    customer_amount = models.IntegerField()
    customer_amount_after_discount = models.IntegerField()
    token_deposit_customer = models.IntegerField()
    token_deposit_HSTC = models.IntegerField()
    token_deposit_date = models.DateField()
    CBM_m3 = models.IntegerField()
    ctns = models.IntegerField()
    gross_weight_kgs = models.IntegerField()
    net_weight_kgs = models.IntegerField()

    def __str__(self):
        return "Customer PI For " + self.customer


