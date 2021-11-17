from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import Auction, Category, Bid
from bootstrap_datepicker_plus import DateTimePickerInput


class AddAuctionForm(forms.ModelForm):
    # FIXME: Need to change both start_date and end_date, use one of these?
    #  - https://simpleisbetterthancomplex.com/tutorial/2019/01/03/how-to-use-date-picker-with-django.html
    name = forms.CharField(max_length=50)
    description = forms.CharField(widget=forms.Textarea)
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=True)
    min_price = forms.IntegerField(label='Minimum start bid')

    class Meta:
        model = Auction
        fields = ['name', 'description', 'category', 'end_date', 'min_price']
        widgets = {
            'end_date': DateTimePickerInput()
        }

    def clean_end_date(self):
        data = self.cleaned_data["end_date"]
        if self.cleaned_data["end_date"] > timezone.now() + timezone.timedelta(days=14):
            raise forms.ValidationError("End date cannot be more than 14 days from now")
        return data


class BidOnAuctionForm(forms.ModelForm):
    value = forms.IntegerField()

    class Meta:
        model = Bid
        fields = ['value']
