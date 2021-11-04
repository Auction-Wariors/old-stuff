from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=40, default='')
    last_name = models.CharField(max_length=50, default='')
    phone_number = models.CharField(max_length=12, default='')
    street_address = models.CharField(max_length=100, default='')
    city = models.CharField(max_length=100, default='')
    zip_code = models.CharField(max_length=5, default='')

    def __str__(self):
        return f'{self.user.username} Profile'
