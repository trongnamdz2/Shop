from django.contrib import admin
from .models import UserExtend, Item, Category, Images, Cart
# Register your models here.
admin.site.register(UserExtend)
admin.site.register(Item)
admin.site.register(Category)
admin.site.register(Images)
admin.site.register(Cart)