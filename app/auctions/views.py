from django.shortcuts import render, redirect
from django.contrib import messages

from auctions.forms import AddAuctionForm


def view_auction(request):
    pass


def add_auction(request):
    if request.method == 'POST':
        form = AddAuctionForm(request.POST)
        if form.is_valid():
            #  FIXME: ADD LOGIC
            messages.success(request, f'Auction added')
            return redirect('stores:view_store')

    else:
        form = AddAuctionForm()
    return render(request, 'auctions/add_auction.html', {'form': form})
