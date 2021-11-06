from django.shortcuts import render, redirect
from django.contrib import messages

from app.users.forms import UserRegisterForm


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account successfully created for user: {username}')
            return redirect('base:login')

    else:
        form = UserRegisterForm()
    return render(request, 'users/register_old.html', {'form': form})


def user_profile(request):
    pass


