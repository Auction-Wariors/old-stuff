from django.shortcuts import render, redirect
from django.contrib import messages
from stores.models import Store


from auctions.forms import AddAuctionForm


def view_auction(request):
    pass


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
