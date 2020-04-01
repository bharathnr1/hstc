from django.urls import path

from . import views

app_name = 'customer'

urlpatterns = [

#main Customer Paths

    path('', views.main_Customer_List.as_view(), name='main_customer-list'),
    path('main_customer-forms/', views.main_Customer_Create, name='main_customer-create'),
    path('main_customer-details/<int:pk>/', views.main_Customer_Detail.as_view(), name='main_customer-detail'),
    path('main_edit/<int:pk>', views.main_Customer_Update.as_view(), name='main_customer-edit'),
    path('main_delete/<int:pk>', views.main_Customer_Delete.as_view(), name="main_customer-delete"),

#Customer Paths

    path('customer-forms/<int:pk>', views.Customer_Create, name='customer-create'),
    path('edit/<int:pk>', views.Customer_Update.as_view(), name='customer-edit'),
    path('delete/<int:pk>', views.Customer_Delete.as_view(), name="customer-delete"),

 
#Customer_PI Paths

    path('sendCPI/<int:pk>', views.send_CPI, name="send_CPI"),
    path('update-customer-PI/<int:pk>', views.CustomerPI_Update.as_view(), name="CustomerPI_Update"),
    path('customer_pi_list/<int:pk>', views.customer_pi_list, name="customer_pi_list"),

#DiliveryDates:
    path('shipment-type/<int:pk>', views.shipment_type, name="shipment_type"),
    path('dilivery-dates/<int:pk>', views.dilivery_dates, name="dilivery_dates"),
    path('updatedates/<int:pk>/<int:id>', views.updatedates, name="updatedates"),
    # path('', views.Vendor_List.as_view(), name='vendor-list'),
    # path('vendor-details/<int:pk>/', views.Vendor_Detail.as_view(), name='vendor-detail'),
    # path('vendor-forms/ThankYou/', views.form_submission, name='form-submit'),
    # path('vendor-edit/<int:pk>', views.Vendor_Update.as_view(), name='vendor-edit'),
    # path('vendor-delete/<int:pk>', views.Vendorr_Delete.as_view(), name="vendor-delete")


]