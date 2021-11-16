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

    # Time left auction, create own function?
    time = auction.end_date - timezone.now()
    print(time)
    time_left = time.total_seconds()

    days = time_left // (24 * 3600)
    time_left = time_left % (24 * 3600)
    hours = time_left // 3600
    time_left %= 3600
    minutes = time_left // 60
    time_left %= 60
    seconds = time_left
    count_down = {
        'days': int(days),
        'hours': int(hours),
        'minutes': int(minutes),
        'seconds': int(seconds)
    }

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
        elif bid.owner == auction.store.owner:
            messages.warning(request, "You are not allowed to bid on your own auctions")
        elif current_leading_bid and bid.owner == current_leading_bid.owner:
            messages.warning(request, "You already have the leading bid!")
        else:
            bid.save()
            print(f"Bid added: {datetime.datetime.now()}")
            print(f"Bid added: {timezone.now()}")
            return redirect('auctions:auction_detail', pk=pk)

    return render(request, 'auctions/auction_detail.html', {'auction': auction,
                                                            'bids': bids,
                                                            'high_bid': leading_bid,
                                                            'time': count_down})


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
