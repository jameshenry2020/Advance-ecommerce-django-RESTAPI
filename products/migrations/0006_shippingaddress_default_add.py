# Generated by Django 3.2.8 on 2022-03-31 21:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_auto_20220329_1529'),
    ]

    operations = [
        migrations.AddField(
            model_name='shippingaddress',
            name='default_add',
            field=models.BooleanField(default=False),
        ),
    ]