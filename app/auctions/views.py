from django.shortcuts import render, redirect
from django.contrib import messages

from auctions.forms import AddAuctionForm, AddItemForm


def view_auction(request):
    pass


def add_auction(request):
    if request.method == 'POST':
        a_form = AddAuctionForm(request.POST)
        i_form = AddItemForm(request.POST)
        if i_form.is_valid() and a_form.is_valid():
            #  FIXME: ADD LOGIC
            messages.success(request, f'Auction added')
            return redirect('stores:view_store')

    else:
        a_form = AddAuctionForm()
        i_form = AddItemForm()
    return render(request, 'auctions/add_auction.html', {'a_form': a_form, 'i_form': i_form})
