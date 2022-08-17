# Generated by Django 3.2.8 on 2022-08-15 08:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_shippingaddress_orders'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shippingaddress',
            name='orders',
        ),
        migrations.AlterField(
            model_name='order',
            name='shippingAd',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='products.shippingaddress'),
        ),
    ]