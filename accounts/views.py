from django.shortcuts import render,redirect
from django.contrib import messages,auth
from django.contrib.auth.models import User
from product.models import Category
from product.models import Product
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
import json
from product.models import *
from product.utils import cookieCart , cartData
from .forms import OrderForm, CreateUserForm
from .decorators import unauthenticated_user, allowed_users, admin_only
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
#from contacts.models import Contact

def login(request):
    data = cartData(request)
    cartItems = data['cartItems']
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            messages.success(request,'you are logged in successfully!')
            return redirect('home')
        else:
            messages.error(request,'invalid credentials')
            return redirect('login')
    else:
        context={'cartItems':cartItems}
        return render(request,'accounts/login.html',context)

def logout(request):
       if request.method=='POST':
        auth.logout(request)
        messages.success(request,'logout successfully')
        return redirect('home')


#def dashboard(request):
#    user_contacts=Contact.objects.order_by('-contact_date').filter(user_id=request.user.id)
#    context={
#    'contacts': user_contacts
#    }
#    return render(request,'accounts/dashboard.html',context)
def register(request):
    data = cartData(request)
    cartItems = data['cartItems']
    if request.method=='POST':
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        password2=request.POST['password2']
        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request,'username already taken')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request,'email already being taken')
                    return redirect('register')
                else:
                    user=User.objects.create_user(first_name=first_name,last_name=last_name,
                    username=username,password=password,email=email)
                    user.save()
                    customer, created = Customer.objects.get_or_create(
                    email=email,
                    )
                    customer.user = user
                    customer.name = username
                    customer.save()
                    messages.success(request,'you are successfully registered')
                    return redirect('login')
                    customer, created = Customer.objects.get_or_create(
                    email=email,
                    )
                    customer.user = user
                    customer.name = name
                    customer.save()

        else:
            messages.error(request,'password did not match')
            return render(request,'accounts/register.html')
    else:
        context={'cartItems':cartItems}
        return render(request,'accounts/register.html',context)
