from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from .forms import LoginForm, RegisterForm

from .models import Item, UserExtend, Images, Category, Cart

from django.contrib.auth import authenticate, login

# Create your views here.

class LoginPage(View):
    def get(self, request):
        if self.request.user.is_authenticated:
            return redirect('home')
        form = LoginForm()
        return render(request, 'base/login.html',{
            'form': form,
        })

    def post(self, request):
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']


            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')

        return render(request, 'base/login.html', {
            'form': form
        })


class Register(View):
    def get(self, request):
        if self.request.user.is_authenticated:
            return redirect('home')
        form = RegisterForm()
        return render(request, 'base/register.html', {
            'form': form
        })

    def post(self, request):
        form = RegisterForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            password = form.cleaned_data['password']
            register = User(username=username, password=make_password(password), first_name=first_name, last_name=last_name)
            register.save()
            user = authenticate(username=username, password=password)
            if user is not None:
                new_user = UserExtend(user=user)
                new_user.save()
                login(request, user)
                return redirect('home')

        return render(request, 'base/register.html', {
            'form': form
        })
    

class HomePage(View):
    def get(self, request):
        if request.GET.get('cart'):
            if self.request.user.is_anonymous:
                return redirect('login')
            self.add_to_cart(request.GET.get('cart'))
            return redirect(self.request.path)
        item_query = Item.objects.filter(status=True).order_by('-created')
        carted = self.carted_item()
        if len(item_query) >= 5:
            newest_item = []
            for i in range(5):
                newest_item.append(item_query[i])
        else:
            newest_item = item_query
        return render(request, 'base/home.html', {
            'new_item': newest_item,
            'carted': carted,
            'category': self.get_category,
        })
    
    def post(self, request):
        pass

    def add_to_cart(self, id):
        item = Item.objects.get(id=id)
        user = self.request.user
        try:
            if Cart.objects.get(user=user, item=item):
                increase_quantity = Cart.objects.get(user=user, item=item)
                increase_quantity.quantity += 1
                increase_quantity.save()
        except:
            add = Cart(user=user, item=item)
            add.save()

    def carted_item(self):
        if self.request.user.is_authenticated:
            user = self.request.user
            amount_item = 0
            user_cart = Cart.objects.filter(user=user, status=0)
            for i in user_cart:
                amount_item += i.quantity
            return amount_item
    
    def get_category(self):
        category = Category.objects.all()
        return category



class ItemDetail(View):
    def get(self, request, pk):
        if request.GET.get('cart'):
            if self.request.user.is_anonymous:
                return redirect('login')
            HomePage.add_to_cart(self, pk)
            return redirect(self.request.path)
        item = Item.objects.get(id=pk)
        item_image = Images.objects.filter(item=item)
        return render(request, 'base/detail.html', {
            'item': item,
            'images': item_image,
            'carted': HomePage.carted_item(self),
            'category': HomePage.get_category(self),
        })
    

class AllItem(View):
    def get(self, request):
        if request.GET.get('cart'):
            if self.request.user.is_anonymous:
                return redirect('login')
            HomePage.add_to_cart(self, request.GET.get('cart'))
            return redirect(self.request.path)
        all_item = Item.objects.all().order_by('-created')
        return render(request, 'base/all_item.html', {
            'category': HomePage.get_category(self),
            'carted': HomePage.carted_item(self),
            'all_item': all_item,
        })

class CategoryDetail(View):
    def get(self, request, slug):
        if request.GET.get('cart'):
            if self.request.user.is_anonymous:
                return redirect('login')
            HomePage.add_to_cart(self, request.GET.get('cart'))
            return redirect(self.request.path)
        category = Category.objects.get(slug=slug)
        all_item = Item.objects.filter(category=category, status=True)
        print(self.request.path)
        return render(request, 'base/category.html', {
            'category': HomePage.get_category(self),
            'carted': HomePage.carted_item(self),
            'specific': category,
            'cate_item': all_item,
        })