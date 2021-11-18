from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages

from auctions.models import Auction
from .models import Profile

from users.forms import UserRegisterForm


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'User created: {username}. You are now logged in.')
            user = authenticate(username=form.cleaned_data['username'],
                                password=form.cleaned_data['password1'])
            login(request, user)
            return redirect('base:index')

    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


def user_profile(request):
    profile = Profile.objects.get(user=request.user)
    winning_auctions = Auction.objects.filter(winner=request.user, isPayed=False).order_by('end_date')
    payed_auctions = Auction.objects.filter(winner=request.user, isPayed=True).order_by('end_date')
    return render(request, 'users/profile.html', {'profile': profile, 'auctions': winning_auctions, 'payed_auctions': payed_auctions})
