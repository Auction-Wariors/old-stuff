from django.db import models
from django.contrib.auth.models import User


class Store(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    description = models.CharField(max_length=1000)
    email = models.EmailField()
    phone_number = models.CharField(max_length=12)

    def __str__(self):
        return self.name

