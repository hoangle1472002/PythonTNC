import datetime
import json
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

from .models import *
from django.http import JsonResponse
from .utils import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib import messages

def create_user(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        email = request.POST.get('email')
        password = request.POST.get('password')
        user, created = Users.objects.get_or_create(username=username, email=email, password=password)
        return render(request, 'store/login.html')
    return render(request, 'store/register.html')


def check_login(request):
    if request.method == 'POST':
        # Lấy dữ liệu từ request
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Kiểm tra username và password
        user = Users.objects.filter(email=email, password=password)
        if len(user) > 0:
            # Nếu hợp lệ, trả về status OK
            return redirect('/store', {'email': email})
        else:
            # Nếu không hợp lệ, trả về status Failed
            return render(request, 'store/login.html')
    return render(request, 'store/login.html')

def logout_view(request):
    logout(request)
    return redirect('/store')

# Create your views here.
def store(request):
    data = cartData(request )
    cartItems = data['cartItems']

    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'store/store.html', context)


def cart(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/cart.html', context)


@csrf_exempt
def checkout(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action : ', action)
    print('ProductId : ', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = orderItem.quantity + 1
    elif action == 'remove':
        orderItem.quantity = orderItem.quantity - 1

    orderItem.save()
    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    else:
        customer, order = guestOrder(request,data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == float(order.get_cart_total):
        order.complete = True
    order.save()
    if order.shipping:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            # state = data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
        )

    return JsonResponse('Payment submitted ... ', safe=False)

def search(request):
    query = request.GET.get('query')
    products = Product.objects.filter(name__icontains=query)
    return render(request, 'store/store.html', {'products': products})