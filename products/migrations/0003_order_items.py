# Generated by Django 3.2.8 on 2022-03-29 08:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_auto_20220322_0044'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='items',
            field=models.ManyToManyField(to='products.OrderItem'),
        ),
    ]
