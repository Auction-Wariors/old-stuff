from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.contrib import messages
from .forms import UserSignUpForm, StoreSignUpForm, AddAuctionForm, AddItemForm
from .models import User, Store, Auction


class UserSignUp(CreateView):
    model = User
    form_class = UserSignUpForm

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        messages.success(self.request, f'Bruker {username} opprettet')
        return redirect('login')


class StoreSignUp(CreateView):
    """
    FIXME: Several users
    """
    model = User
    form_class = StoreSignUpForm

    def form_valid(self, form):
        form.save()
        username = form.cleaned_data.get('username')
        messages.success(self.request, f'Bruker {username} opprettet')
        return redirect('login')


def add_item(request):
    if request.method == 'POST':
        owner = request.user.id
        store_name = Store.objects.get(owner=owner)
        a_form = AddAuctionForm(request.POST)
        i_form = AddItemForm(request.POST)
        if i_form.is_valid() and a_form.is_valid():
            item = i_form.save()
            item_name = i_form.cleaned_data['name']
            Auction.objects.create(item=item, start_date=a_form.cleaned_data['start_date'],
                                   end_date=a_form.cleaned_data['end_date'],
                                   min_price=a_form.cleaned_data['min_price'],
                                   store=store_name)
            messages.success(request, f'Item {item_name} added')
            return redirect('store')

    else:
        a_form = AddAuctionForm()
        i_form = AddItemForm()
    return render(request, 'base/add_auction.html', {'a_form': a_form, 'i_form': i_form})


def index(request):
    return render(request, 'base/index.html')

def view_auction(request):
    """
    View a single auction, if a store owner views an auction, the template displays an edit button
    PUT will edit auction
    DELETE will...
    """
    pass


def add_auction(request):
    pass



def store(request):
    """
    Profile page
    """
    owner = request.user.id
    store_name = Store.objects.get(owner=owner)
    auctions = Auction.objects.all().filter(store=store_name)
    return render(request, 'base/store_profile.html', {'store': store_name, 'auctions': auctions})


def store_edit(request):
    return None
