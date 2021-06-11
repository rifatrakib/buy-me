from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import *
from .forms import *

# def home(request):
#     return render(request, 'market/home.html')


class ProductView(View):
    def get(self, request):
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        electronics = Product.objects.filter(category='Electronics')
        food_and_bevarage = Product.objects.filter(category='Food & Bevarage')
        furniture = Product.objects.filter(category='Furniture')
        stationary = Product.objects.filter(category='Stationary')
        decoration = Product.objects.filter(category='Decoration')
        clothes = Product.objects.filter(category='Clothes')
        accessories = Product.objects.filter(category='Accessories')
        return render(
            request,
            'market/home.html',
            {
                'electronics': electronics,
                'food_and_bevarage': food_and_bevarage,
                'furniture': furniture,
                'stationary': stationary,
                'decoration': decoration,
                'clothes': clothes,
                'accessories': accessories,
                'totalitem': totalitem,
            }
        )


# def product_detail(request):
#     return render(request, 'market/product-detail.html')

class ProductDetailView(View):
    def get(self, request, pk):
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        product = Product.objects.get(pk=pk)
        item_already_in_cart = False
        if request.user.is_authenticated:
            item_already_in_cart = Cart.objects.filter(
                Q(product=product.id) & Q(user=request.user)).exists()
        return render(
            request,
            'market/product-detail.html',
            {
                'product': product,
                'item_already_in_cart': item_already_in_cart,
                'totalitem': totalitem,
            }
        )


@login_required()
def add_to_cart(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    return redirect('/cart', {'totalitem': totalitem, })


@login_required()
def show_cart(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        user = request.user
        cart = Cart.objects.filter(user=user)
        print(cart)
        amount = 0.0
        shipping = 70.0
        cart_products = list(cart)
        if cart_products:
            for p in cart_products:
                temp_amount = (p.quantity * p.product.discounted_price)
                amount += temp_amount
            return render(
                request, 'market/add-to-cart.html',
                {'carts': cart, 'amount': amount, 'totalamount': amount +
                    shipping, 'totalitem': totalitem, }
            )
        else:
            return render(request, 'market/empty-cart.html', {'totalitem': totalitem, })


def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity += 1
        c.save()
        amount = 0.0
        shipping = 70.0
        cart_product = list(Cart.objects.filter(user=request.user))
        for p in cart_product:
            temp_amount = (p.quantity * p.product.discounted_price)
            amount += temp_amount
        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': amount + shipping,
        }
        return JsonResponse(data)
    else:
        return JsonResponse('')


def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity -= 1
        c.save()
        amount = 0.0
        shipping = 70.0
        cart_product = list(Cart.objects.filter(user=request.user))
        for p in cart_product:
            temp_amount = (p.quantity * p.product.discounted_price)
            amount += temp_amount
        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': amount + shipping,
        }
        return JsonResponse(data)
    else:
        return JsonResponse('')


def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        amount = 0.0
        shipping = 70.0
        cart_product = list(Cart.objects.filter(user=request.user))
        for p in cart_product:
            temp_amount = (p.quantity * p.product.discounted_price)
            amount += temp_amount
        data = {
            'amount': amount,
            'totalamount': amount + shipping,
        }
        return JsonResponse(data)
    else:
        return JsonResponse('')


def buy_now(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'market/buy-now.html', {'totalitem': totalitem, })


# def profile(request):
#     return render(request, 'market/profile.html')
@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        form = CustomerProfileForm()
        return render(request, 'market/profile.html', {'form': form, 'active': 'btn-primary', 'totalitem': totalitem, })

    def post(self, request):
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            usr = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(
                user=usr, name=name, locality=locality,
                city=city, state=state, zipcode=zipcode,
            )
            reg.save()
            messages.success(
                request, 'Congratulations! Profile updated successfully.')
        return render(request, 'market/profile.html', {'form': form, 'active': 'btn-primary', 'totalitem': totalitem, })


@login_required()
def address(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    add = Customer.objects.filter(user=request.user)
    return render(request, 'market/address.html', {'add': add, 'active': 'btn-primary', 'totalitem': totalitem, })


@login_required()
def orders(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    op = OrderPlaced.objects.filter(user=request.user)
    return render(request, 'market/orders.html', {'order_placed': op, 'totalitem': totalitem, })


def change_password(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'market/change-password', {'totalitem': totalitem, })


def product(request, data=None):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    if data == None:
        products = Product.objects.all()
    else:
        products = Product.objects.filter(category=data)
    return render(request, 'market/product.html', {'products': products, 'totalitem': totalitem, })


# def login(request):
#     return render(request, 'market/login.html')


# def register(request):
#     return render(request, 'market/register.html')
class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'market/register.html', {'form': form})

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(
                request, 'Congratulations! Registered successfully')
            form.save()
        return render(request, 'market/register.html', {'form': form})


@login_required()
def checkout(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    amount = 0.0
    shipping = 70.0
    cart_product = list(cart_items)
    for p in cart_product:
        temp_amount = (p.quantity * p.product.discounted_price)
        amount += temp_amount
    return render(
        request, 'market/checkout.html',
        {
            'add': add,
            'totalamount': amount + shipping,
            'cart_items': cart_items,
            'totalitem': totalitem,
        },
    )


@login_required()
def payment_done(request):
    user = request.user
    customer_id = request.GET['custid']
    customer = Customer.objects.get(id=customer_id)
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(
            user=user, customer=customer,
            product=c.product, quantity=c.quantity,
        ).save()
        c.delete()
    return redirect('orders')
