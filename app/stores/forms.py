from django import forms
from .models import Store


class CreateStoreForm(forms.ModelForm):

    class Meta:
        model = Store
        # TODO: More fields?
        fields = ['name', 'description', 'email', 'phone_number']
