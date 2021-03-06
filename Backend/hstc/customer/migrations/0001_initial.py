# Generated by Django 3.0.4 on 2020-04-24 13:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_name', models.CharField(max_length=30)),
                ('customer_contact', models.IntegerField()),
                ('customer_email', models.EmailField(max_length=254)),
                ('customer_company', models.CharField(max_length=100)),
                ('shipment_type', models.CharField(blank=True, choices=[('One Shipment', 'One Shipment'), ('Part Shipments', 'Part Shipments')], max_length=50, null=True)),
                ('shipment_file', models.FileField(blank=True, null=True, upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Customer_Details',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('s_no', models.IntegerField(blank=True, null=True)),
                ('list_no', models.IntegerField(blank=True, null=True)),
                ('sub_list_no', models.IntegerField(blank=True, null=True)),
                ('company_name', models.CharField(blank=True, max_length=100, null=True)),
                ('contact_no', models.IntegerField(blank=True, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('wechat', models.IntegerField(blank=True, null=True)),
                ('invoice_date', models.DateField(blank=True, null=True)),
                ('invoice_no', models.CharField(blank=True, max_length=100, null=True)),
                ('description', models.CharField(blank=True, max_length=200, null=True)),
                ('model', models.CharField(blank=True, max_length=100, null=True)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='')),
                ('dimensions', models.CharField(blank=True, max_length=100, null=True)),
                ('remarks', models.CharField(blank=True, max_length=200, null=True)),
                ('unit', models.CharField(blank=True, max_length=200, null=True)),
                ('unit_price', models.IntegerField(blank=True, null=True)),
                ('qty', models.IntegerField(blank=True, null=True)),
                ('customer_amount', models.IntegerField(blank=True, null=True)),
                ('customer_amount_after_discount', models.IntegerField(blank=True, null=True)),
                ('commission_persentage', models.CharField(blank=True, max_length=100, null=True)),
                ('commission_rmb', models.IntegerField(blank=True, null=True)),
                ('actual_vendor_amount', models.IntegerField(blank=True, null=True)),
                ('vendor_deposit_persentage', models.IntegerField(blank=True, null=True)),
                ('vendor_advance_deposit_amount', models.IntegerField(blank=True, null=True)),
                ('token_deposit_customer', models.IntegerField(blank=True, null=True)),
                ('token_deposit_HSTC', models.IntegerField(blank=True, null=True)),
                ('token_deposit_date', models.DateField(blank=True, null=True)),
                ('vendor_advance_balance', models.IntegerField(blank=True, null=True)),
                ('vendor_advance_balance_paid', models.IntegerField(blank=True, null=True)),
                ('advance_balance_date', models.DateField(blank=True, null=True)),
                ('vendor_final_balance', models.IntegerField(blank=True, null=True)),
                ('vendor_final_balance_date', models.DateField(blank=True, null=True)),
                ('account_details', models.CharField(blank=True, max_length=200, null=True)),
                ('manufacturing_days', models.IntegerField(blank=True, null=True)),
                ('CBM_m3', models.IntegerField(blank=True, null=True)),
                ('ctns', models.CharField(blank=True, max_length=100, null=True)),
                ('gross_weight_kgs', models.IntegerField(blank=True, null=True)),
                ('net_weight_kgs', models.IntegerField(blank=True, null=True)),
                ('shipment_number', models.IntegerField(blank=True, null=True)),
                ('tentative_dilivery_date', models.DateField(blank=True, null=True)),
                ('planned_inspection_date', models.DateField(blank=True, null=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.Customer')),
            ],
        ),
        migrations.CreateModel(
            name='Inspection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('actual_inspection_date', models.DateField(blank=True, null=True)),
                ('planned_inspection_date', models.DateField(blank=True, null=True)),
                ('inspection_done_by', models.CharField(blank=True, max_length=300, null=True)),
                ('inspection_remarks', models.CharField(blank=True, max_length=300, null=True)),
                ('inspection_photo_1', models.ImageField(blank=True, null=True, upload_to='')),
                ('inspection_photo_2', models.ImageField(blank=True, null=True, upload_to='')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.Customer')),
                ('vendor_company_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.Customer_Details')),
            ],
        ),
        migrations.CreateModel(
            name='Container_loading',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo1', models.ImageField(blank=True, null=True, upload_to='')),
                ('photo2', models.ImageField(blank=True, null=True, upload_to='')),
                ('photo3', models.ImageField(blank=True, null=True, upload_to='')),
                ('PortDetails1', models.CharField(blank=True, max_length=200, null=True)),
                ('PortDetails2', models.CharField(blank=True, max_length=200, null=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.Customer')),
                ('vendor_company_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.Customer_Details')),
            ],
        ),
    ]
