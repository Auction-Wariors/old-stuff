from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from auctions.models import Auction, Bid
from .models import Profile

from users.forms import UserRegisterForm, ProfileForm, UserEditForm


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


@login_required
def user_profile(request):
    profile = Profile.objects.get(user=request.user)
    winning_auctions = Auction.objects.filter(winner=request.user, is_payed=False).order_by('end_date')
    payed_auctions = Auction.objects.filter(winner=request.user, is_payed=True).order_by('end_date')
    bids = Bid.objects.filter(owner=request.user)
    return render(request, 'users/profile.html', {'profile': profile,
                                                  'auctions': winning_auctions,
                                                  'payed_auctions': payed_auctions,
                                                  'bids': bids})


@login_required
def update_profile(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        user_form = UserEditForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('users:user_profile')
            
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileForm(instance=profile)

        return render(request, 'users/edit_profile.html', {'profile_form': profile_form, 'user_form': user_form})
    