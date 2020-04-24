from django.db import models

ENTRY_CHOICES = (
    ('One Shipment','One Shipment'),
    ('Part Shipments','Part Shipments'),
)


class Customer(models.Model):
    customer_name = models.CharField(max_length=30)
    customer_contact = models.IntegerField()
    customer_email = models.EmailField()
    customer_company = models.CharField(max_length=100)
    shipment_type = models.CharField(max_length=50, choices=ENTRY_CHOICES, blank=True, null=True)
    shipment_file = models.FileField(blank=True, null=True)

    def __str__(self):
        return self.customer_name

    def get_absolute_url(self):
        x=self.pk
        return f'/customer/main_customer-details/{x}'


class Customer_Details(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    s_no = 	models.IntegerField(blank=True, null=True)
    list_no = models.IntegerField(blank=True, null=True)
    sub_list_no =models.IntegerField(blank=True, null=True)
    company_name= models.CharField(max_length=100,blank=True, null=True)
    contact_no = models.IntegerField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    wechat = models.IntegerField(blank=True, null=True)
    invoice_date = models.DateField(blank=True, null=True)
    invoice_no = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=200,blank=True, null=True)
    model = models.CharField(max_length=100,blank=True, null=True)
    photo = models.ImageField(blank=True, null=True)
    dimensions = models.CharField(max_length=100,blank=True, null=True)
    remarks = models.CharField(max_length=200,blank=True, null=True)
    unit = models.CharField(max_length=200,blank=True, null=True)
    unit_price = models.IntegerField(blank=True, null=True)
    qty = models.IntegerField(blank=True, null=True)
    customer_amount = models.IntegerField(blank=True, null=True)
    customer_amount_after_discount =models.IntegerField(blank=True, null=True)
    commission_persentage = models.CharField(max_length=100, blank=True, null=True)
    commission_rmb = models.IntegerField(blank=True, null=True)
    actual_vendor_amount =models.IntegerField(blank=True, null=True)
    vendor_deposit_persentage= models.IntegerField(blank=True, null=True)
    vendor_advance_deposit_amount =models.IntegerField(blank=True, null=True)
    token_deposit_customer =models.IntegerField(blank=True, null=True)
    token_deposit_HSTC =models.IntegerField(blank=True, null=True)
    token_deposit_date = models.DateField(blank=True, null=True)
    vendor_advance_balance =models.IntegerField(blank=True, null=True)
    vendor_advance_balance_paid =models.IntegerField(blank=True, null=True)
    advance_balance_date =models.DateField(blank=True, null=True)
    vendor_final_balance =models.IntegerField(blank=True, null=True)
    vendor_final_balance_date =models.DateField(blank=True, null=True)
    account_details =models.CharField(max_length=200,blank=True, null=True)
    manufacturing_days =models.IntegerField(blank=True, null=True)
    CBM_m3 =models.IntegerField(blank=True, null=True)
    ctns =models.CharField(max_length=100, blank=True, null=True)
    gross_weight_kgs =models.IntegerField(blank=True, null=True)
    net_weight_kgs =models.IntegerField(blank=True, null=True)
    shipment_number = models.IntegerField(blank=True, null=True)
    tentative_dilivery_date = models.DateField(blank=True, null=True)
#Need to remove planeed inspection date
    planned_inspection_date = models.DateField(blank=True, null=True)
 
    def __str__(self):
        return str(self.company_name)
    
    def get_absolute_url(self):
        x= self.customer.pk
        return f'/customer/main_customer-details/{x}'


class Inspection(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    vendor_company_name = models.ForeignKey(Customer_Details, on_delete=models.CASCADE)   
    actual_inspection_date = models.DateField(blank=True, null=True)
    planned_inspection_date = models.DateField(blank=True, null=True)
    inspection_done_by  = models.CharField(max_length=300, blank=True,  null=True)
    inspection_remarks = models.CharField(max_length=300, blank=True,  null=True)
    inspection_photo_1 = models.ImageField(blank=True,  null=True)
    inspection_photo_2 = models.ImageField(blank=True,  null=True)

    def __str__(self):
        return str(self.vendor_company_name)


class Container_loading(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    vendor_company_name = models.ForeignKey(Customer_Details, on_delete=models.CASCADE)
    photo1 = models.ImageField(blank=True, null=True)
    photo2 = models.ImageField(blank=True, null=True)
    photo3 = models.ImageField(blank=True, null=True)
    PortDetails1 = models.CharField(max_length=200,blank=True, null=True)
    PortDetails2 = models.CharField(max_length=200,blank=True, null=True)

    def __str__(self):
        return str(self.vendor_company_name)
