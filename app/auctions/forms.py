from django import forms
from .models import Auction, Category


class AddAuctionForm(forms.ModelForm):
    # FIXME: Need to change both start_date and end_date, use one of these?
    #  - https://simpleisbetterthancomplex.com/tutorial/2019/01/03/how-to-use-date-picker-with-django.html
    name = forms.CharField(max_length=50)
    description = forms.CharField(widget=forms.Textarea)
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=True)
    start_date = forms.DateTimeField(label='Start date')
    end_date = forms.DateTimeField(label='End date')
    min_price = forms.IntegerField(label='Minimum start bid')

    class Meta:
        model = Auction
        fields = ['name', 'description', 'category', 'start_date', 'end_date', 'min_price']
