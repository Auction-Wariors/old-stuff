from django.db import models
from django.contrib.auth.models import User


class Store(models.Model):
    # FIXME: enforce int/format of phone number
    name = models.CharField(max_length=100, default='Storename')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner')
    moderators = models.ManyToManyField(User, related_name='moderator', blank=True)
    description = models.CharField(max_length=1000, default='')
    email = models.EmailField(default='')
    phone_number = models.CharField(max_length=12, default='')

    def __str__(self):
        return self.name

