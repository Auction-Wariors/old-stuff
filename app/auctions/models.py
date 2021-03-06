from django.db import models
from django.contrib.auth.models import User

from stores.models import Store


class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=250, blank=True, null=True)

    def __str__(self):
        return self.name


class Auction(models.Model):
    """
    Note: All values are stored in NOK -> "øre".
    Finance services usually require cent/øre as currency values
    """
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=5000)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    store = models.ForeignKey(Store, on_delete=models.DO_NOTHING)
    is_active = models.BooleanField(default=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    highest_bid = models.IntegerField(null=True, blank=True)
    winner = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    is_payed = models.BooleanField(default=False)
    commission_is_payed = models.BooleanField(default=False)
    min_price = models.IntegerField()
    buy_now = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return "Auction: " + self.name


class Bid(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    value = models.IntegerField()

    auction = models.ForeignKey(Auction, on_delete=models.SET_NULL, null=True)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Auction: {self.auction.name} Bid: {self.value}"
