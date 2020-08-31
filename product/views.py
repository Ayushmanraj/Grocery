from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
import json
from .models import *
import datetime
from .utils import cookieCart , cartData , guestOrder
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib import messages
from decimal import *
from django.forms import DecimalField
# Create your views here.
def category(request):
    data = cartData(request)

    cartItems = data['cartItems']
    category=Category.objects.all()
    context={'category':category,'cartItems':cartItems}

    return render(request,'products/category.html',context)

def product(request,id):
    data = cartData(request)

    cartItems = data['cartItems']
    category=get_object_or_404(Category,pk=id)
    product=Product.objects.filter(category=category)
    context={'product':product,'cartItems':cartItems}
    return render(request,'products/products.html',context)

def productdetail(request,id):
    product=get_object_or_404(Product,pk=id)
    return render(request,'products/product_detail.html',{'product':product})

def search(request):
    data = cartData(request)

    cartItems = data['cartItems']
    query_list=Product.objects.order_by('listing_date')

    if 'keywords' in request.GET:
        keywords=request.GET['keywords']
        if keywords:
            query_list=query_list.filter(description__icontains=keywords)
    context={'product':query_list,'cartItems':cartItems}
    return render(request,'products/search.html',context)


def cart(request):

    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items,'order':order,'cartItems':cartItems }
    return render(request,'products/cart.html',context)

def checkout(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items,'order':order ,'cartItems':cartItems}
    return render(request, 'products/checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action:', action)
    print('Product:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
        messages.success(request,'Item Added To Cart Successfully !!')
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
        messages.success(request,'Item Removed From Cart Successfully !!')
    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was Added', safe=False)

def processOrder(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    context = {'items': items,'order':order ,'cartItems':cartItems}
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        

    else:
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == float(order.get_cart_total):
       order.complete = True
    order.save()

    if order.shipping == True:
       ShippingAddress.objects.create(
             customer=customer,
             order=order,
             address=data['shipping']['address'],
             city=data['shipping']['city'],
             tel=data['shipping']['tel'],
             zipcode=data['shipping']['zipcode'],
             )

    to = request.POST.get('email')
    carttotal = order.get_cart_total
    cartItems = order.get_cart_items
    customerName = order.customer.name
    customerEmail = order.customer.email
    customerAddress=data['shipping']['address']
    customerCity=data['shipping']['city']
    customerTel=data['shipping']['tel']
    customerZipcode=data['shipping']['zipcode']




    html_content = render_to_string("products/send_mail.html",{'title':'order_details','items': items,'order':order ,'cartItems':cartItems,'carttotal':carttotal,'cartItems':cartItems,'customerName':customerName,'customerEmail':customerEmail,'customerAddress':customerAddress,'customerCity':customerCity,'customerTel':customerTel,'customerZipcode':customerZipcode})
    text_content = strip_tags(html_content)
    email = EmailMultiAlternatives(
    "order details",
    text_content,
    customerEmail,
    [settings.EMAIL_HOST_USER]
    )
    email.attach_alternative(html_content,"text/html")
    email.send()
    if request.user.is_authenticated:
        points = Decimal(order.get_cart_total) * Decimal(0.01)
        customer.points = Decimal(customer.points) + points
        customer.save()

    return JsonResponse('Order has been placed', safe=False)

def sendmail(request,context):

    if request.method == "POST":
        to = request.POST.get('email')
        content=order.get_cart_total
        html_content = render_to_string("products/send_mail.html",{'title':'order_details', 'content':content})
        text_content = strip_tags(html_content)
        email = EmailMultiAlternatives(
        "order details",
        text_content,
        settings.EMAIL_HOST_USER,
        ['ayushmanketan@gmail.com']
        )
        email.attach_alternative(html_content,"text/html")
        email.send()
    #context = {'items': items,'order':order ,'cartItems':cartItems}
    #return render(request, 'products/send_mail.html', context)
