from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from auctions.models import Auction, Bid
from .models import Store

from stores.forms import CreateStoreForm


def view_all_stores(request):
    return render(request, 'stores/index.html')


@login_required()
def create_store(request):
    user_has_store = Store.objects.filter(owner=request.user)
    if user_has_store:
        return redirect('stores:store_dashboard')

    if request.method == 'POST':
        form = CreateStoreForm(request.POST)
        if form.is_valid():
            store = form.save(commit=False)
            store.owner = request.user
            form.save()
            messages.success(request, f'{store.name} added')
            return redirect('stores:store_dashboard')
    else:
        form = CreateStoreForm()
    return render(request, 'stores/create_store.html', {'form': form})


@login_required()
def store_dashboard(request):
    store = get_object_or_404(Store, owner=request.user)
    auctions_active = Auction.objects.filter(store=store, is_active=True)
    auctions_ended = Auction.objects.filter(store=store, is_active=False)
    return render(request, 'stores/dashboard.html', {'store': store,
                                                     'auctions': auctions_active,
                                                     'auctions_ended': auctions_ended})


@login_required
def update_store_profile(request):
    store = get_object_or_404(Store, owner=request.user)
    if request.method == 'POST':
        form = CreateStoreForm(request.POST, instance=store)
        if form.is_valid():
            form.save()
            return redirect('stores:store_dashboard')
    else:
        form = CreateStoreForm(instance=store)

    return render(request, 'stores/update_store.html', {'form': form})
