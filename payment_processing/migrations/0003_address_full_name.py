# Generated by Django 4.2 on 2023-05-24 06:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment_processing', '0002_remove_order_item'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='full_name',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
