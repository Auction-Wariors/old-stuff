from django import forms
from django.utils import timezone
from flatpickr import DateTimePickerInput
from .models import Auction, Category, Bid


class AddAuctionForm(forms.ModelForm):
    name = forms.CharField(max_length=50)
    description = forms.Textarea()
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=True)
    min_price = forms.IntegerField(label='Minimum start bid in NOK')
    buy_now = forms.IntegerField(label='Buy now price in NOK - Leave empty if auction only', required=False)

    class Meta:
        model = Auction
        fields = ['name', 'description', 'category', 'end_date', 'min_price', 'buy_now']
        widgets = {
            'end_date': DateTimePickerInput()
        }

    def clean_end_date(self):
        date = self.cleaned_data["end_date"]
        if date > timezone.now() + timezone.timedelta(days=14):
            raise forms.ValidationError("End date and time cannot be more than 14 days from now")
        elif date < timezone.now() + timezone.timedelta(minutes=5):
            raise forms.ValidationError("End date and time must be at least 5 minutes from now")
        return date

    def clean_min_price(self):
        return self.cleaned_data["min_price"] * 100

    def clean_buy_now(self):
        return self.cleaned_data["buy_now"] * 100


class UpdateAuctionForm(forms.ModelForm):
    name = forms.CharField(max_length=50)
    description = forms.Textarea()
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=True)
    min_price = forms.IntegerField(label='Minimum start bid')

    class Meta:
        model = Auction
        fields = ['name', 'description', 'category', 'min_price']

    def __init__(self, *args, **kwargs):
        bid = kwargs.pop('bid')
        super(UpdateAuctionForm, self).__init__(*args, **kwargs)
        if bid:
            del self.fields['min_price']

    def clean_min_price(self):
        return self.cleaned_data["min_price"] * 100



class BidOnAuctionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.auction_id = kwargs.pop('auction_id')
        self.user = kwargs.pop('user')
        super(BidOnAuctionForm, self).__init__(*args, **kwargs)

    value = forms.IntegerField(label='Your bid')

    class Meta:
        model = Bid
        fields = ['value']

    def clean_value(self):
        value = self.cleaned_data["value"]
        auction = Auction.objects.get(pk=self.auction_id)
        if not auction.highest_bid:
            auction.highest_bid = 0

        if value < auction.min_price / 100:
            raise forms.ValidationError("Bid is too low")
        elif value < auction.highest_bid / 100:
            raise forms.ValidationError("Bid is too low")
        elif timezone.now() > auction.end_date:
            raise forms.ValidationError("Auction is ended")
        elif auction.store.owner == self.user:
            raise forms.ValidationError("Bidding on your own auction is not allowed")
        return value * 100
