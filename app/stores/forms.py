from django import forms

from .models import Store


class CreateStoreForm(forms.ModelForm):

    name = forms.CharField(max_length=50)
    description = forms.CharField(widget=forms.Textarea)
    email = forms.EmailField()
    phone_number = forms.NumberInput()

    class Meta:
        model = Store

        fields = ['name', 'description', 'email', 'phone_number']

    def clean(self):
        data = self.cleaned_data
        name = data["name"]
        store_name = Store.objects.filter(name=name)

        if store_name.exists():
            raise forms.ValidationError('Store name already exits')
