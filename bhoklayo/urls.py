from django.urls import path
from . import views

urlpatterns = [
    path('',               views.index,        name='index'),
    path('menu/',          views.menu,         name='menu'),
    path('add/<int:id>/',  views.add_to_cart,  name='add_to_cart'),
    path('cart/',          views.view_cart,    name='view_cart'),
    path('order/',         views.place_order,  name='place_order'),
    path('esewa/pay/',     views.esewa_pay,    name='esewa_pay'),
    path('esewa/verify/',  views.esewa_verify, name='esewa_verify'),
    path('failed/',        views.order_failed, name='order_failed'),
    path('confirm/',       views.confirmation, name='confirmation'),
]
