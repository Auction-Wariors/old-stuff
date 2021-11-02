from django.shortcuts import render
from auctions.models import Auction


def index(request):
    auctions = Auction.objects.all()
    return render(request, 'base/index.html', {'auctions': auctions})


def login(request):
    return render(request, 'base/login.html')
