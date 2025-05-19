import requests
from django.shortcuts import render, redirect
from django.urls import reverse
from django.conf import settings
from .models import Category, MenuItem, Order

def index(request):
    return render(request, 'bhoklayo/index.html')

def menu(request):
    categories = Category.objects.all()
    items      = MenuItem.objects.all()
    return render(request, 'bhoklayo/menu.html', {
        'categories': categories,
        'items': items
    })

def add_to_cart(request, id):
    cart = request.session.get('cart', [])
    cart.append(id)
    request.session['cart'] = cart
    return redirect('menu')

def view_cart(request):
    ids   = request.session.get('cart', [])
    items = MenuItem.objects.filter(id__in=ids)
    total = sum(item.price for item in items)
    return render(request, 'bhoklayo/cart.html', {
        'items': items,
        'total': total
    })

def place_order(request):
    if request.method == 'POST':
        order = Order.objects.create(
            name     = request.POST['name'],
            email    = request.POST['email'],
            address  = request.POST['address'],
            city     = request.POST['city'],
            zip_code = request.POST['zip'],
        )
        order.items.set(MenuItem.objects.filter(id__in=request.session.get('cart', [])))
        order.save()
        request.session['order_id'] = order.id
        return redirect('esewa_pay')
    return render(request, 'bhoklayo/order.html')

def esewa_pay(request):
    order   = Order.objects.get(id=request.session['order_id'])
    amt     = float(sum(item.price for item in order.items.all()))
    success = request.build_absolute_uri(reverse('esewa_verify'))
    failure = request.build_absolute_uri(reverse('order_failed'))
    return render(request, 'bhoklayo/esewa_pay.html', {
        'order': order,
        'amount': f'{amt:.2f}',
        'merchant': settings.ESEWA_MERCHANT_CODE,
        'success': success,
        'failure': failure,
    })

def esewa_verify(request):
    data = {
        'amt': request.POST.get('amt'),
        'pid': request.POST.get('pid'),
        'rid': request.POST.get('rid'),
        'scd': request.POST.get('scd'),
    }
    res = requests.post('https://esewa.com.np/epay/main', data=data)
    if 'Success' in res.text:
        order = Order.objects.get(id=data['pid'])
        order.is_paid = True
        order.save()
        request.session['cart'] = []
        return redirect('confirm')
    return redirect('order_failed')

def order_failed(request):
    return render(request, 'bhoklayo/order_failed.html')

def confirmation(request):
    return render(request, 'bhoklayo/confirmation.html')
