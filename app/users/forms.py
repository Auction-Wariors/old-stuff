from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class UserEditForm(forms.ModelForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class ProfileForm(forms.ModelForm):
    phone_number = forms.CharField(max_length=12, required=False)
    street_address = forms.CharField(max_length=100, required=False)
    city = forms.CharField(max_length=100,required=False)
    zip_code = forms.CharField(max_length=5, required=False)

    class Meta:
        model = Profile
        fields = ['phone_number', 'street_address', 'city', 'zip_code']
