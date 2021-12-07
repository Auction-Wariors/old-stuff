from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


def add_users():
    for x in range(3):
        User.objects.get_or_create(username=f'User {x+1}', password=make_password('pw2022'))


class Command(BaseCommand):
    def handle(self, **options):
        add_users()
