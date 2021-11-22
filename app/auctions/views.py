from django.contrib.auth.decorators import login_required
from django.db.models import Max
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib import messages
from stores.models import Store
from .models import Auction, Bid

from auctions.forms import AddAuctionForm


def auction_detail(request, pk):
    auction = get_object_or_404(Auction, pk=pk)
    bids = Bid.objects.filter(auction=auction)
    current_leading_value = bids.aggregate(Max('value'))
    current_leading_bid = Bid.objects.filter(auction=auction, value__exact=current_leading_value["value__max"]).first()

    # Extracted in own function
    count_down = count_down_func(auction)

    if not current_leading_bid:
        leading_bid = auction.min_price - 1
    else:
        leading_bid = current_leading_bid.value

    if request.method == 'POST':
        bid = Bid(owner=request.user, auction=auction, value=int(request.POST['bid_value']))
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
            bid.auction.highest_bid = bid.value
            bid.auction.save()
            bid.save()
            return redirect('auctions:auction_detail', pk=pk)

    return render(request, 'auctions/auction_detail.html', {'auction': auction,
                                                            'bids': bids,
                                                            'high_bid': leading_bid,
                                                            'time': count_down})


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
        form = AddAuctionForm(request.POST, instance=auction)
        if form.is_valid():
            form.save()
            return redirect('stores:store_dashboard')
    else:
        form = AddAuctionForm(instance=auction)

    return render(request, 'auctions/update_auction.html', {'form': form})


def count_down_func(auction):
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
    return count_down
