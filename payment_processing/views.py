from django.shortcuts import render, redirect
from django.views.generic.base import View

from .forms import AddressForm

from .models import Order, Address

from base.views import HomePage

# Create your views here.

class Cart(View):
    def get(self, request):
        if self.request.user.is_anonymous:
            return redirect('login')
        if request.GET.get('increase-func'):
            id = request.GET['increase-func']
            item = self.request.user.cart.get(id=id, status=0)
            item.quantity += 1
            item.save()
            return redirect(self.request.path)
        elif request.GET.get('decrease-func'):
            id = request.GET['decrease-func']
            item = self.request.user.cart.get(id=id, status=0)
            if item.quantity > 1:
                item.quantity -= 1
                item.save()
                return redirect(self.request.path)
            else:
                item.delete()
                return redirect(self.request.path)
        elif request.GET.get('delete_item_cart'):
            id = request.GET['delete_item_cart']
            item = self.request.user.cart.get(id=id, status=0)
            item.delete()
            return redirect(self.request.path)
        user_cart = self.request.user.cart.filter(status=0)
        subtotal = []
        total_quantity = []
        for i in user_cart:
            price = int(i.item.price) * int(i.quantity)
            subtotal.append(price)
            total_quantity.append(i.quantity)
        return render(request, 'payment/cart.html', {
            'carted': HomePage.carted_item(self),
            'user_cart': user_cart,
            'subtotal': sum(subtotal),
            'quantity': sum(total_quantity),
            'category': HomePage.get_category(self),
        })

class Checkout(View):
    def get(self, request):
        if self.request.user.is_anonymous:
            return redirect('login')
        address_form = AddressForm()
        user_cart = self.request.user.cart.filter(status=0)
        subtotal = []
        total_quantity = []
        for i in user_cart:
            price = int(i.item.price) * int(i.quantity)
            subtotal.append(price)
            total_quantity.append(i.quantity)
        tax = sum(subtotal)*10/100
        return render(request, 'payment/checkout.html', {
            'carted': HomePage.carted_item(self),
            'address_form': address_form,
            'user_cart': user_cart,
            'tax': int(tax),
            'total': sum(subtotal) + int(tax),
            'quantity': sum(total_quantity),
            'category': HomePage.get_category(self),
        })
    
    def post(self, request):
        address_form = AddressForm(request.POST)
        all_carted_item = self.request.user.cart.filter(status=0)
        user_cart = self.request.user.cart.filter(status=0)
        subtotal = []
        total_quantity = []
        for i in user_cart:
            price = int(i.item.price) * int(i.quantity)
            subtotal.append(price)
            total_quantity.append(i.quantity)
        tax = sum(subtotal)*10/100
        total = int(sum(subtotal)) + int(tax)
        print(total)
        if total <= 0:
            return redirect('home')
        elif address_form.is_valid():
            full_name = address_form.cleaned_data['full_name']
            address = address_form.cleaned_data['address']
            phone_numb = address_form.cleaned_data['sdt']
            method = address_form.cleaned_data['method']

            new_address = Address(user=self.request.user, address=address, sdt=phone_numb, full_name=full_name)
            new_address.save()

            new_order = Order(user=self.request.user, address=new_address, method=method, price=total, quantity=sum(total_quantity))
            new_order.save()

            for i in all_carted_item:
                i.status = 1
                i.order = new_order
                i.name_order = i.item.title
                i.item = None
                i.save()
            return render(request, 'payment/success.html', {
                'id': new_order.id,
            })

        return render(request, 'payment/checkout.html', {
            'address_form': address_form,
            'user_cart': user_cart,
        })
    

class OrderHistory(View):
    def get(self, request):
        return render(request, 'payment/history.html')