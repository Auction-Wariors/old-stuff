from django.shortcuts import render
from auctions.models import Auction


def index(request):
    auctions = Auction.objects.all()
    return render(request, 'base/index.html', {'auctions': auctions})


def pricing(request):
    return render(request, 'base/pricing.html')


def login(request):
    return render(request, 'base/login.html')


def register(request):
    return render(request, 'base/register.html')
