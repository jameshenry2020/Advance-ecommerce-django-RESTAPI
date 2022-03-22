# Generated by Django 3.2.8 on 2022-03-21 23:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='itemvariation',
            unique_together={('variation', 'value')},
        ),
        migrations.AlterUniqueTogether(
            name='variation',
            unique_together={('item', 'name')},
        ),
    ]