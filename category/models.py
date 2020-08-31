
from django.db import models
from datetime import datetime
# Create your models here.
# Create your models here.
class Category(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100,blank=True)
    Main_photo=models.ImageField(upload_to='photo/',blank=False)

    def __str__(self):
        return self.first_name
