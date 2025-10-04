from django.db import models
from django.contrib.auth.models import User

class Menu(models.Model):
   item_name = models.CharField(max_length=200) 
   price = models.IntegerField(null=False) 
   menu_item_description = models.TextField(max_length=1000, default='') 
   image = models.ImageField(upload_to='menu_images/', blank=True, null=True)
   type = models.CharField(max_length=200, blank=True, null=True)
   
   def __str__(self):
        return self.item_name

class Booking(models.Model):
    name = models.CharField(max_length=200)
    reservation_date = models.DateField()
    reservation_slot = models.SmallIntegerField()
    amt_people = models.SmallIntegerField()

class checkout(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)