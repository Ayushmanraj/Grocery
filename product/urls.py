from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.category,name='category'),
    path('<int:id>',views.product,name='product'),
    path('search',views.search,name='search'),
    path('update_item/', views.updateItem, name="update_item"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('product/<int:id>',views.productdetail,name='productdetail'),
    path('process_order/', views.processOrder, name="process_order"),
    path('send_mail/', views.sendmail, name="process_order"),
    ]
