from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render
from django.contrib import messages

from auctions.models import Auction, Category


def index(request):
    auctions = Auction.objects.order_by('-start_date').filter(is_active=True)
    categories = Category.objects.all()
    param_user = request.GET.get('user', '')

    if param_user == 'StoreUser2':
        logout(request)
        user = authenticate(username='StoreUser2',
                            password='StoreUser2')
        login(request, user)
        messages.success(request, 'StoreUser1 logged in! ')

    if param_user == 'User3':
        logout(request)
        user = authenticate(username='User3',
                            password='User3')
        login(request, user)
        messages.success(request, 'User3 logged in! ')

    if param_user == 'User4':
        logout(request)
        user = authenticate(username='User4',
                            password='User4')
        login(request, user)
        messages.success(request, 'User4 logged in! ')

    return render(request, 'base/index.html', {'auctions': auctions, 'categories': categories})


def pricing(request):
    return render(request, 'base/pricing.html')


def faq(request):
    return render(request, 'base/faq.html')


def about(request):
    return render(request, 'base/about.html')
