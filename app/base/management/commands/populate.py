from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
import random

from auctions.models import Category, Auction, Bid
from stores.models import Store


def add_store_users():
    for x in range(2):
        try:
            User.objects.get(pk=f'{x + 1}')
        except User.DoesNotExist:
            user = User.objects.create(username=f'StoreUser{x + 1}', password=make_password(f'StoreUser{x + 1}'))
            user.first_name = f'StoreUser{x + 1}'
            user.last_name = 'LastName'
            user.email = f'user{x + 1}@mail.com'
            user.save()


def add_end_users():
    for x in range(3, 6):
        try:
            User.objects.get(pk=f'{x}')
        except User.DoesNotExist:
            user = User.objects.create(username=f'User{x}', password=make_password(f'User{x}'))
            user.first_name = f'User{x}'
            user.last_name = 'LastName'
            user.email = f'user{x}@mail.com'
            user.save()


def add_admin():
    try:
        User.objects.get(username='admin')
    except User.DoesNotExist:
        admin = User.objects.create(username='admin', password=make_password('admin'))
        admin.is_superuser = True
        admin.is_staff = True
        admin.is_active = True
        admin.save()


def add_stores():
    for x in range(2):
        try:
            Store.objects.get(pk=f'{x + 1}')
        except Store.DoesNotExist:
            Store.objects.create(name=f'StoreUser{x + 1}´s Store',
                                 owner=User.objects.get(pk=f'{x + 1}'),
                                 description=f'User{x + 1}Store Description',
                                 email=f'User{x + 1}Store@store.com',
                                 phone_number='+4755555555')


def add_categories():
    for x in range(3):
        Category.objects.get_or_create(name=f'Category {x + 1}')


def add_active_auctions():
    for x in range(5):
        Auction.objects.get_or_create(name=f'Auction {x + 1}',
                                      description=f'Auction {x + 1} description',
                                      category=Category.objects.get(pk=random.randint(1, 3)),
                                      store=Store.objects.get(pk=1),
                                      start_date=timezone.now(),
                                      end_date=timezone.now() + timezone.timedelta(days=14),
                                      min_price=10000,
                                      buy_now=50000)
    for x in range(5, 10):
        Auction.objects.get_or_create(name=f'Auction {x + 1}',
                                      description=f'Auction {x + 1} description',
                                      category=Category.objects.get(pk=random.randint(1, 3)),
                                      store=Store.objects.get(pk=2),
                                      start_date=timezone.now(),
                                      end_date=timezone.now() + timezone.timedelta(days=14),
                                      min_price=25000)

    Auction.objects.get_or_create(name=f'Auction 11',
                                  description=f'Auction 11 description',
                                  category=Category.objects.get(pk=random.randint(1, 3)),
                                  store=Store.objects.get(pk=2),
                                  start_date=timezone.now(),
                                  end_date=timezone.now() + timezone.timedelta(minutes=5),
                                  min_price=30000)


def add_bids():
    # Add bids to auction 2
    Bid.objects.create(value=27000,
                       auction=Auction.objects.get(pk=2),
                       owner=User.objects.get(pk=4))

    Bid.objects.create(value=30000,
                       auction=Auction.objects.get(pk=2),
                       owner=User.objects.get(pk=3))
    auction1 = Auction.objects.get(pk=2)
    auction1.highest_bid = 30000
    auction1.save()

    # Add bids to auction 10
    Bid.objects.create(value=30000,
                       auction=Auction.objects.get(pk=10),
                       owner=User.objects.get(pk=3))
    Bid.objects.create(value=35000,
                       auction=Auction.objects.get(pk=10),
                       owner=User.objects.get(pk=5))
    Bid.objects.create(value=40000,
                       auction=Auction.objects.get(pk=10),
                       owner=User.objects.get(pk=3))
    auction2 = Auction.objects.get(pk=10)
    auction2.highest_bid = 40000
    auction2.save()

    # Add bids to auction 11
    Bid.objects.create(value=30000,
                       auction=Auction.objects.get(pk=11),
                       owner=User.objects.get(pk=3))
    Bid.objects.create(value=35000,
                       auction=Auction.objects.get(pk=11),
                       owner=User.objects.get(pk=5))
    auction3 = Auction.objects.get(pk=11)
    auction3.highest_bid = 35000
    auction3.save()


def buy_now_auction():
    auction = Auction.objects.get(pk=3)
    user3 = User.objects.get(pk=3)
    auction.winner = user3
    auction.highest_bid = auction.buy_now
    auction.end_date = timezone.now()
    auction.is_active = False
    auction.save()


class Command(BaseCommand):
    def handle(self, **options):
        try:
            User.objects.get(username='admin')
            print("DB already up to date")
        except User.DoesNotExist:
            add_store_users()
            add_end_users()
            add_admin()
            add_stores()
            add_categories()
            add_active_auctions()
            add_bids()
            buy_now_auction()
            print("Populate database completed...")
