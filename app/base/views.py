from django.shortcuts import render
from auctions.models import Auction
from auctions.views import check_auction


def index(request):
    check_auction()
    auctions = Auction.objects.order_by('-start_date').filter(is_active=True)

    return render(request, 'base/index.html', {'auctions': auctions})


def pricing(request):
    return render(request, 'base/pricing.html')


def faq(request):
    return render(request, 'base/faq.html')


def login(request):
    return render(request, 'base/login.html')

