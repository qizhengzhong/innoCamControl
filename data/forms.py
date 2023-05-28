        
from django import forms
from django.forms import ModelForm
from .models import Data

class DataForm(forms.ModelForm):
    required_css_class = 'required'
    class Meta:
        model = Data
        fields = ['number','week','sku','weekly_sales','EV','color','price','vendor','functionality']
