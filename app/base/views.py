from django.shortcuts import render
from auctions.models import Auction, Category, Bid
from django.utils import timezone


def index(request):
    check_auction()
    auctions = Auction.objects.order_by('-start_date').filter(is_active=True)
    categories = Category.objects.all()

    return render(request, 'base/index.html', {'auctions': auctions, 'categories': categories})


def pricing(request):
    return render(request, 'base/pricing.html')


def faq(request):
    return render(request, 'base/faq.html')



def check_auction():
    auctions = Auction.objects.all()
    bids = Bid.objects.all()
    for auction in auctions:
        if timezone.now() > auction.end_date and auction.is_active:
            auction.is_active = False
            winning_bid = bids.filter(auction=auction).last()
            if winning_bid is not None:
                auction.winner = winning_bid.owner
            auction.save()
