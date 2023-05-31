from django.db import models
from django.contrib.auth.models import User

from payment_processing.models import Order

# Create your models here.
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='notify', null=True)
    title = models.CharField(max_length=100, blank=True)
    detail = models.TextField()
    date = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.title
    
class Category(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    slug = models.SlugField(null=True)
    def __str__(self):
        return self.name
    

class Item(models.Model):
    title = models.CharField(max_length=200, null=True)
    description = models.TextField()
    thumbnail = models.ImageField(upload_to='images', null=True, blank=True)
    price = models.IntegerField()
    category = models.ManyToManyField(Category, blank=True)
    status = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.title
    
class Images(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=True, related_name='img')
    image = models.ImageField(upload_to='images', null=True, blank=True)
    
    def __str__(self):
        return f'Image of {self.item.title}'
    
class UserExtend(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='info')
    admin = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
    

class Cart(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True, related_name='order')
    name_order = models.CharField(max_length=1000, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart')
    item = models.OneToOneField(Item, on_delete=models.CASCADE, related_name='cart', null=True)
    quantity = models.IntegerField(default=1)
    status = models.IntegerField(default=0, null=True)

    def __str__(self):
        return self.user.username
    

