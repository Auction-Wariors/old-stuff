"""



"""
from datetime import datetime

from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class Store(models.Model):
    name = models.CharField(max_length=100, default='Storename')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner')
    moderators = models.ManyToManyField(User, related_name='moderator')
    description = models.CharField(max_length=1000, default='')
    email = models.EmailField(default='')
    phone_number = models.CharField(max_length=12, default='')

    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=5000)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Auction(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    buy_now_price = models.BigIntegerField()
    start_date = models.DateTimeField(default=datetime.now())
    end_date = models.DateTimeField(default=datetime.now())
    winner = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True)
    isPayed = models.BooleanField(default=False)
    min_price = models.IntegerField(default=0)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, default='')

    def __str__(self):
        return "Auction: " + self.item.name


class Bid(models.Model):
    """Finance services require cent/øre as currency values"""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    value = models.BigIntegerField()
    max_value = models.BigIntegerField()  # If user wants automatic bidding (up to max_value)

    auction = models.ForeignKey(Auction, on_delete=models.DO_NOTHING)
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING)


    def __str__(self):
        return f"Auction: {self.auction.item.name} Bid: {self.value}"
