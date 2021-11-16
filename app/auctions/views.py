from django.contrib.auth.decorators import login_required
from django.db.models import Max
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib import messages
from stores.models import Store
from .models import Auction, Bid
import datetime


from auctions.forms import AddAuctionForm


def auction_detail(request, pk):
    auction = get_object_or_404(Auction, pk=pk)
    bids = Bid.objects.filter(auction=auction)
    current_leading_value = bids.aggregate(Max('value'))
    current_leading_bid = Bid.objects.filter(auction=auction, value__exact=current_leading_value["value__max"]).first()

    if not current_leading_bid:
        leading_bid = auction.min_price-1
    else:
        leading_bid = current_leading_bid.value

    if request.method == 'POST' and 'bid_value' in request.POST:
        bid = Bid()
        bid.owner = request.user
        bid.auction = auction
        bid.value = int(request.POST['bid_value'])
        bid.max_value = 2
        if bid.value <= leading_bid:
            messages.warning(request, "Bid is too low")
            # FIXME: Add javascript in template?
        elif timezone.now() > auction.end_date:
            # Auction ended
            messages.warning(request, "Auction is ended")
        else:
            bid.save()
            print(f"Bid added: {datetime.datetime.now()}")
            print(f"Bid added: {timezone.now()}")
            return redirect('auctions:auction_detail', pk=pk)

    return render(request, 'auctions/auction_detail.html', {'auction': auction,
                                                            'bids': bids,
                                                            'high_bid': leading_bid})


@login_required
def add_auction(request):
    if request.method == 'POST':
        form = AddAuctionForm(request.POST)
        if form.is_valid():
            auction = form.save(commit=False)
            user = request.user
            auction.store = Store.objects.get(owner=user)
            auction.start_date = timezone.now()
            auction.save()
            messages.success(request, f'Auction added')
            return redirect('stores:store_dashboard')

    else:
        form = AddAuctionForm()
    return render(request, 'auctions/add_auction.html', {'form': form})
