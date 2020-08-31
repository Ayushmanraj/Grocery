from __future__ import unicode_literals
from django.db import models
from datetime import datetime
from category.models import Category
from django.contrib.auth.models import User

# Create your models here.

class Product(models.Model):
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    product_name=models.CharField(max_length=100)
    mrp_price=models.DecimalField(max_digits=7,decimal_places=2)
    our_price=models.DecimalField(max_digits=7,decimal_places=2)
    Main_photo=models.ImageField(upload_to='photo/',blank=False)
    size=models.CharField(max_length=100)
    listing_date=models.DateTimeField(default=datetime.now,blank=True)
    is_topselling=models.BooleanField(default=False)
    description=models.TextField(default="")
    def __str__(self):
        return self.product_name

class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    points = models.DecimalField(max_digits=7,decimal_places=2,default=0)


    def __str__(self):
        return self.name


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    #product = models.ManyToManyField(Product, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            shipping = True
        return shipping

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.our_price * self.quantity
        return total

class ShippingAddress(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	address = models.CharField(max_length=200, null=False)
	city = models.CharField(max_length=200, null=False)
	tel = models.CharField(max_length=200, null=False)
	zipcode = models.CharField(max_length=200, null=False)
	date_added = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.address

#class OrderDetails(models.Model):
    #customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    #order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    #address=mode
