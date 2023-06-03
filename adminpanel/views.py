from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.views.generic.list import ListView
from django.utils.text import slugify
from .forms import AddItemForm, AddCategoryForm, category

from base.models import Item, Images, Category, Cart
from payment_processing.models import Order

# Create your views here.


class AdminPage(View):
    def get(self, request):
        if not self.user_validator():
            return redirect('home')
        return render(request, 'adminpanel/admin.html')
    
    def user_validator(self):
        if self.request.user.is_anonymous or not self.request.user.info.admin:
            return False
        return True
    
class PostItem(View):
    def get(self, request):
        if not AdminPage.user_validator(self):
            return redirect('home')
        form = AddItemForm()
        return render(request, 'adminpanel/additem.html', {
            'form': form,
        })
    
    def post(self, request):
        form = AddItemForm(request.POST, request.FILES)

        if form.is_valid():
            field = {}
            images = request.FILES.getlist('images')
            for i in form:
                field[i.name] = form.cleaned_data[i.name]
            create_item = Item(
                title=field['name'], 
                description=field['description'], 
                thumbnail=field['thumbnail'],
                price=field['price'],
            )
            create_item.save()
            for i in field['category']:
                query_category = Category.objects.get(name=i)
                create_item.category.add(query_category.id)
            
            for image in images:
                post_image = Images(image=image, item=create_item)
                post_image.save()
        
        return render(request, 'adminpanel/additem.html', {
            'form': form
        })
    

class CreatedItem(ListView):
    model = Item
    template_name = 'adminpanel/createditem.html'
    context_object_name = 'item'

    def get_context_data(self, **kwargs):
        context = super(CreatedItem, self).get_context_data(**kwargs)
        context['item'] = context['item'].order_by('-id')
        return context
    
    def get(self, request, *args, **kwargs):
        if not AdminPage.user_validator(self):
            return redirect('home')
        return super().get(self, request, *args, **kwargs)

    
class AddCategory(View):
    def get(self, request):
        if not AdminPage.user_validator(self):
            return redirect('home')
        form = AddCategoryForm()
        return render(request, 'adminpanel/addcategory.html', {
            'form': form,
        })
    
    def post(self, request):
        form = AddCategoryForm(request.POST)
        
        if form.is_valid():
            cate_name = form.cleaned_data['name']
            cate_slug = slugify(cate_name)
            new_category = Category(name=cate_name, slug=cate_slug)
            new_category.save()
        return render(request, 'adminpanel/addcategory.html', {
            'form': form,
        })
    


class AllOrder(View):
    def get(self, request):
        if not AdminPage.user_validator(self):
            return redirect('home')
        all_order = Order.objects.all().order_by('-id')
        return render(request, 'adminpanel/allorder.html', {
            'all_order': all_order
        })
    
class ProcessOrder(View):
    def get(self, request, id):
        if not AdminPage.user_validator(self):
            return redirect('home')
        if request.GET.get('duyet'):
            id = request.GET['duyet']
            current_order = Order.objects.get(id=id)
            current_order.status = 1
            current_order.save()
            return redirect('order')
        elif request.GET.get('xoa'):
            id = request.GET['xoa']
            current_order = Order.objects.get(id=id)
            current_order.delete()
            return redirect('order')
        order = Order.objects.get(id=id)
        item = Cart.objects.filter(order=order)
        return render(request, 'adminpanel/processorder.html', {
            'order': order,
            'item': item,
        })
