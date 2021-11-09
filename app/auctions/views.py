from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from stores.models import Store
from .models import Auction, Bid


from auctions.forms import AddAuctionForm


def auction_detail(request, pk):
    auction = get_object_or_404(Auction, pk=pk)
    bids = Bid.objects.filter(auction=auction)
    return render(request, 'auctions/auction_detail.html', {'auction': auction, 'bids': bids})


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
