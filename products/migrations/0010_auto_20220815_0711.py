# Generated by Django 3.2.8 on 2022-08-15 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_auto_20220815_0133'),
    ]

    operations = [
        migrations.AddField(
            model_name='transactionhistory',
            name='status',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='transactionhistory',
            name='stripe_customer_id',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
