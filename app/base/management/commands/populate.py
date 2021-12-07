from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from auctions.models import Category


def add_admin():
    try:
        User.objects.get(username='admin')
    except User.DoesNotExist:
        admin = User.objects.create(username='admin', password=make_password('admin'))
        admin.is_superuser = True
        admin.is_staff = True
        admin.is_active = True
        admin.save()


def add_end_users():
    for x in range(3):
        try:
            User.objects.get(username=f'User {x + 1}')
        except User.DoesNotExist:
            user = User.objects.create(username=f'User{x + 1}', password=make_password(f'User{x + 1}'))
            user.first_name = f'User{x + 1}'
            user.last_name = 'LastName'
            user.email = f'user{x + 1}@mail.com'
            user.save()


def add_store_users():
    for x in range(2):
        try:
            User.objects.get(username=f'StoreUser{x + 1}')
        except User.DoesNotExist:
            user = User.objects.create(username=f'StoreUser{x + 1}', password=make_password(f'StoreUser{x + 1}'))
            user.first_name = f'StoreUser{x + 1}'
            user.last_name = 'LastName'
            user.email = f'user{x + 1}@mail.com'
            user.save()


def add_categories():
    for x in range(3):
        Category.objects.get_or_create(name=f'Category {x+1}')


class Command(BaseCommand):
    def handle(self, **options):
        add_admin()
        add_end_users()
        add_store_users()
        add_categories()
        print("Populate database completed...")
