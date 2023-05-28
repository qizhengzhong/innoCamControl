from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL),]
    operations = [migrations.CreateModel(name='Data',fields=[
    ('number', models.DecimalField(max_digits=7,decimal_places=0,blank=True,primary_key = True)),
    ('week', models.CharField(max_length=100,blank=True)),
    ('sku', models.CharField(max_length=100,blank=True)),
    ('weekly_sales', models.CharField(max_length=100,blank=True)),
    ('EV', models.CharField(max_length=100,blank=True)),
    ('color', models.CharField(max_length=100,blank=True)),
    ('price', models.CharField(max_length=100,blank=True)),
    ('vendor', models.CharField(max_length=100,blank=True)),
    ('functionality', models.CharField(max_length=100,blank=True)),
            ],
        ),
    ]
