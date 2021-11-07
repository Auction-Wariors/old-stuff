from django import forms
from .models import Store


class CreateStoreForm(forms.ModelForm):
    # TODO: Display name of the user creating the store in the form
    # TODO: Let creator select moderator/manager based on email?

    name = forms.CharField(max_length=50)
    description = forms.CharField(widget=forms.Textarea)
    email = forms.EmailField()
    phone_number = forms.NumberInput()

    class Meta:
        model = Store
        # TODO: More fields?
        fields = ['name', 'description', 'email', 'phone_number']
