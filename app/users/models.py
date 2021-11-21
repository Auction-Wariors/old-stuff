from django.db import models
from django.contrib.auth import get_user_model


class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=12, default='')
    street_address = models.CharField(max_length=100, default='')
    city = models.CharField(max_length=100, default='')
    zip_code = models.CharField(max_length=5, default='')

    def __str__(self):
        return f"{self.user.username}'s Profile"
