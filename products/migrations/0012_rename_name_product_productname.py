# Generated by Django 3.2.8 on 2022-08-19 07:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0011_alter_product_rating'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='name',
            new_name='productname',
        ),
    ]