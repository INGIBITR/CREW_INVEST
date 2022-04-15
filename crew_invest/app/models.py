from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.FloatField(default=0)
    avatar = models.ImageField(upload_to='images/', blank=True,default='-1.jpeg')


class Stock(models.Model):
    name = models.CharField(max_length=255)
    amount = models.IntegerField(default=1)
    owner = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='stocks')


class StockPage(models.Model):
    ticker = models.CharField(max_length=255)
    price = models.IntegerField()
    pricechange = models.IntegerField()
    

