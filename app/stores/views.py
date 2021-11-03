from django.shortcuts import render
from django.contrib import messages

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
    else:
        form = CreateStoreForm()
    return render(request, 'stores/create_store.html', {'form': form})


def view_store(request):
    return render(request, 'stores/storeinfo.html')


def add_auction(request):
    pass
