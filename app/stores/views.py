from django.shortcuts import render, redirect
from django.contrib import messages

from auctions.models import Auction, Bid
from .models import Store

from stores.forms import CreateStoreForm


def view_all_stores(request):
    return render(request, 'stores/index.html')


def create_store(request):
    if request.method == 'POST':
        form = CreateStoreForm(request.POST)
        if form.is_valid():
            store = form.save(commit=False)
            store.owner = request.user
            form.save()
            messages.success(request, f'Store {store.name} added')
            return redirect('stores:store_dashboard')
    else:
        form = CreateStoreForm()
    return render(request, 'stores/create_store.html', {'form': form})


def view_store(request):
    return render(request, 'stores/storeinfo.html')


def store_dashboard(request):
    store = Store.objects.get(owner=request.user)
    auctions_active = Auction.objects.filter(store=store)
    return render(request, 'stores/dashboard.html', {'store': store, 'auctions': auctions_active})


def add_auction(request):
    pass
