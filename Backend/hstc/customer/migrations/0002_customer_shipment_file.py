# Generated by Django 2.2.1 on 2020-04-05 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='shipment_file',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]
