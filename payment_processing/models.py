from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='address')
    full_name = models.CharField(max_length=200, null=True)
    address = models.CharField(max_length=100)
    sdt = models.IntegerField()

    def __str__(self):
        return f"{self.user.username}'s address"
    

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='order')
    address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='order')
    method = models.CharField(max_length=100)
    price = models.IntegerField(null=True)
    quantity = models.IntegerField(null=True)
    status = models.IntegerField(default=0)
    date = models.DateField(auto_now_add=True, null=True)

    def __str__(self):
        return f'Order #{self.id}'
