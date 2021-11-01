from django import forms
from .models import Item, Auction, Category


class AddItemForm(forms.ModelForm):
    name = forms.CharField(max_length=50)
    description = forms.CharField(widget=forms.Textarea)
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=True)

    class Meta:
        model = Item
        fields = ['name', 'description', 'category']


class AddAuctionForm(forms.ModelForm):
    # FIXME: Need to change both start_date and end_date, use one of these?
    #  - https://simpleisbetterthancomplex.com/tutorial/2019/01/03/how-to-use-date-picker-with-django.html
    start_date = forms.DateTimeField(label='Start date')
    end_date = forms.DateTimeField(label='End date')
    min_price = forms.IntegerField(label='Minimum start bid')

    class Meta:
        model = Auction
        fields = ['start_date', 'end_date', 'min_price']