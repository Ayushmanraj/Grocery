from django.shortcuts import render
from product.models import Category
from product.models import Product
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
import json
from product.models import *
from product.utils import cookieCart , cartData
from django.core.mail import send_mail
from django.conf import settings
from .models import *
from django.contrib import messages

# Create your views here.
def home(request):
    data = cartData(request)
    cartItems = data['cartItems']


    product=Product.objects.order_by('-listing_date')[:8]
    context={'product':product,'cartItems':cartItems}
    return render(request,'pages/index.html',context)

def aboutus(request):
    data = cartData(request)
    cartItems = data['cartItems']

    context={'cartItems':cartItems}
    return render(request,'pages/aboutus.html',context)

def contact(request):
    data = cartData(request)
    cartItems = data['cartItems']
    if request.method == 'POST':
        email= request.POST['email']
        fname= request.POST['firstname']
        lname= request.POST['lastname']
        content = request.POST['message']
        message = f"firstname-{fname}  lastname-{lname} email-{email}    message-{content}"

        send_mail('Contact Form',message,email,[settings.EMAIL_HOST_USER],fail_silently=False)
        messages.success(request,'Message sent successfully !!')
    context={'cartItems':cartItems}
    return render(request,'pages/contact.html',context)

def points(request):
    data = cartData(request)
    cartItems = data['cartItems']
    reward=Reward.objects.all()
    context={'cartItems':cartItems,'reward':reward}
    return render(request,'pages/points.html',context)
