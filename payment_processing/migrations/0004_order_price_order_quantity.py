# Generated by Django 4.2 on 2023-05-24 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment_processing', '0003_address_full_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='price',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='quantity',
            field=models.IntegerField(null=True),
        ),
    ]
