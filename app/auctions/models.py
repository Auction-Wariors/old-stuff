from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

from app.stores.models import Store


class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class Auction(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=5000)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    buy_now_price = models.BigIntegerField(default=0)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    winner = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True)
    isPayed = models.BooleanField(default=False)
    min_price = models.IntegerField(default=0)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, default='')

    def __str__(self):
        return "Auction: " + self.name


class Bid(models.Model):
    """Finance services require cent/øre as currency values"""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    value = models.BigIntegerField()
    max_value = models.BigIntegerField()  # If user wants automatic bidding (up to max_value)

    auction = models.ForeignKey(Auction, on_delete=models.DO_NOTHING)
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f"Auction: {self.auction.name} Bid: {self.value}"
