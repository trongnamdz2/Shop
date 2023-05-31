# Generated by Django 4.2 on 2023-05-20 16:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('payment_processing', '0002_remove_order_item'),
        ('base', '0021_cart_name_order_alter_cart_item'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='order', to='payment_processing.order'),
        ),
    ]
