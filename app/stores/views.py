from django.shortcuts import render


def view_all_stores(request):
    return render(request, 'stores/index.html')


def create_store(request):
    pass


def view_store(request):
    return render(request, 'stores/storeinfo.html')


def add_auction(request):
    pass
