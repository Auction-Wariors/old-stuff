from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from stores.models import Store
from .models import Auction, Bid


from auctions.forms import AddAuctionForm, BidOnAuctionForm


def auction_detail(request, pk):
    auction = get_object_or_404(Auction, pk=pk)
    bids = Bid.objects.filter(auction=auction)
    if request.method == 'POST':
        form = BidOnAuctionForm(request.POST)
        if form.is_valid():
            bid = form.save(commit=False)
            bid.owner = request.user
            bid.auction = auction
            bid.max_value = 2  # FIXME: Needs to fix logic
            bid.save()
    else:
        form = BidOnAuctionForm()
    return render(request, 'auctions/auction_detail.html', {'auction': auction, 'bids': bids, 'form': form})


def add_auction(request):
    if request.method == 'POST':
        form = AddAuctionForm(request.POST)
        if form.is_valid():
            auction = form.save(commit=False)
            user = request.user
            auction.store = Store.objects.get(owner=user)
            auction.save()
            messages.success(request, f'Auction added')
            return redirect('stores:view_store')

    else:
        form = AddAuctionForm()
    return render(request, 'auctions/add_auction.html', {'form': form})
