import math

from django.contrib.auth.decorators import login_required
from django.db.models import Max
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib import messages
from stores.models import Store
from .models import Auction, Bid
from logic import count_down_func

from auctions.forms import AddAuctionForm, UpdateAuctionForm, BidOnAuctionForm


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


@login_required()
def buy_now(request, auction_id):
    auction = get_object_or_404(Auction, pk=auction_id)
    if request.user == auction.store.owner:
        return redirect('stores:store_dashboard')

    if auction.highest_bid and auction.highest_bid >= auction.buy_now:
        return redirect('auctions:auction_detail', pk=auction_id)

    if request.POST:
        if auction.buy_now and auction.is_active:
            auction.winner = request.user
            auction.is_active = False
            auction.highest_bid = auction.buy_now
            auction.end_date = timezone.now()
            auction.save()
            messages.success(request, f'Item bought, make sure to make payment to store {auction.store.name}')
            return redirect('users:user_profile')
        else:
            messages.warning(request, 'Auction not active...')

    return render(request, 'auctions/buy_now.html', {'auction': auction})


@login_required
def payment_auction(request, auction_id):
    auction = get_object_or_404(Auction, pk=auction_id, winner=request.user)
    if auction.is_payed:
        return redirect('users:user_profile')

    if request.POST:
        messages.warning(request, 'Payment failed, please contact your bank! '
                                  'Click green button to test successful payment')
        return redirect('auctions:payment_auction', auction_id=auction_id)

    return render(request, 'auctions/payment.html', {'auction': auction})


@login_required
def payment_ok(request, auction_id):
    auction = get_object_or_404(Auction, pk=auction_id, winner=request.user)
    auction.is_payed = True
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

    has_bid = True if auction.highest_bid else False
    if request.method == 'POST':
        form = UpdateAuctionForm(request.POST,
                                 instance=auction,
                                 bid=has_bid)
        if form.is_valid():
            form.save()

            messages.success(request, 'Auction successfully updated')
            return redirect('stores:store_dashboard')

    form = UpdateAuctionForm(instance=auction,
                             bid=has_bid,
                             initial={'min_price': math.ceil(auction.min_price / 100)})

    return render(request, 'auctions/update_auction.html', {'form': form})


