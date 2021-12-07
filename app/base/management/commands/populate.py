from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


def add_users():
    for x in range(3):
        try:
            User.objects.get(username=f'User {x + 1}')
        except User.DoesNotExist:
            user = User.objects.create(username=f'User {x + 1}')
            user.set_password = make_password('pw2022')


class Command(BaseCommand):
    def handle(self, **options):
        add_users()
        print("Populate database completed...")
