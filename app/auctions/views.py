import math

from django.contrib.auth.decorators import login_required
from django.db.models import Max
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib import messages
from stores.models import Store
from .models import Auction, Bid

from auctions.forms import AddAuctionForm, UpdateAuctionForm, UpdateNoBidsAuctionForm, BidOnAuctionForm


def auction_detail(request, pk):
    auction = get_object_or_404(Auction, pk=pk)
    bids = Bid.objects.filter(auction=auction)
    current_leading_value = bids.aggregate(Max('value'))
    current_leading_bid = Bid.objects.filter(auction=auction, value__exact=current_leading_value["value__max"]).first()

    # Extracted in own function
    time = auction.end_date - timezone.now()
    count_down = count_down_func(time)

    if not current_leading_bid:
        leading_bid = auction.min_price - 1
    else:
        leading_bid = current_leading_bid.value

    if auction.highest_bid:
        form = BidOnAuctionForm(initial={'value': math.ceil(auction.highest_bid/100) + 5},
                                auction_id=auction.id,
                                user=request.user)
    else:
        form = BidOnAuctionForm(initial={'value': math.ceil(auction.min_price / 100)},
                                auction_id=auction.id,
                                user=request.user)

    if request.method == 'POST':
        form = BidOnAuctionForm(request.POST, auction_id=auction.id, user=request.user)
        if form.is_valid():
            bid = form.save(commit=False)
            bid.owner = request.user
            bid.auction = auction
            bid.save()
            auction.highest_bid = bid.value
            auction.save()

            return redirect('auctions:auction_detail', pk=pk)

    return render(request, 'auctions/auction_detail.html', {'auction': auction,
                                                            'bids': bids,
                                                            'high_bid': leading_bid,
                                                            'time': count_down,
                                                            'form': form})


@login_required
def payment_auction(request, auction_id):
    auction = get_object_or_404(Auction, pk=auction_id, winner=request.user)
    if auction.isPayed:
        return redirect('users:user_profile')

    if request.POST:
        messages.warning(request, 'Payment failed, please contact your bank! '
                                  'Click green button to test successful payment')
        return redirect('auctions:payment_auction', auction_id=auction_id)

    return render(request, 'auctions/payment.html', {'auction': auction})


@login_required
def payment_ok(request, auction_id):
    auction = get_object_or_404(Auction, pk=auction_id, winner=request.user)
    auction.isPayed = True
    auction.save()
    messages.success(request, f'Payment successful! Total amount payed: NOK {auction.highest_bid},- ')
    return redirect('users:user_profile')


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


@login_required
def update_auction(request, auction_id):
    store = Store.objects.get(owner=request.user)
    auction = Auction.objects.get(store=store, pk=auction_id)
    if not auction or not auction.is_active:
        return redirect('stores:store_dashboard')
    if request.method == 'POST':
        if auction.highest_bid:
            form = UpdateAuctionForm(request.POST, instance=auction)
        else:
            form = UpdateNoBidsAuctionForm(request.POST, instance=auction)

        if form.is_valid():
            form.save()
            return redirect('stores:store_dashboard')
    elif auction.highest_bid:
        form = UpdateAuctionForm(instance=auction)
    else:
        # FIXME / 100 is hardcoded, dont have enough experience with currency.
        form = UpdateNoBidsAuctionForm(instance=auction, initial={'min_price': math.ceil(auction.min_price / 100)})

    return render(request, 'auctions/update_auction.html', {'form': form})


def count_down_func(time):
    # FIXME: Do this frontend with JS!!!!
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
    return count_down
