from django.contrib import admin
from django.urls import path,include
from .import views

urlpatterns = [
    path('',views.home,name='home'),
    path('aboutus',views.aboutus,name='aboutus'),
    path('contact',views.contact,name='contact'),
    path('points',views.points,name='points'),

    ]
