from django.db import models
from django.contrib.auth.models import User

class Data(models.Model):
    number=models.DecimalField(max_digits=7,decimal_places=0,blank=True,primary_key = True)
    week=models.DateField(blank=True)
    sku=models.DecimalField(max_digits=7,decimal_places=2,blank=True)
    weekly_sales=models.DecimalField(max_digits=7,decimal_places=2,blank=True)
    EV=models.CharField(max_length=100,blank=True)
    color=models.CharField(max_length=100,blank=True)
    price=models.DecimalField(max_digits=7,decimal_places=2,blank=True)
    vendor=models.DecimalField(max_digits=7,decimal_places=2,blank=True)
    functionality=models.CharField(max_length=100,blank=True)

    def __str__(self):
        return str(self.number)
