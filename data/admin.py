        
from django.contrib import admin
from .models import Data

class DataAdmin(admin.ModelAdmin):
    list_display = ['week','sku','weekly_sales','EV','color','price','vendor','functionality']
admin.site.register(Data, DataAdmin)
