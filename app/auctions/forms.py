from django import forms
from django.utils import timezone
from flatpickr import DateTimePickerInput
from .models import Auction, Category, Bid


class AddAuctionForm(forms.ModelForm):
    name = forms.CharField(max_length=50)
    description = forms.Textarea()
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=True)
    min_price = forms.IntegerField(label='Minimum start bid')

    class Meta:
        model = Auction
        fields = ['name', 'description', 'category', 'end_date', 'min_price']
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


class BidOnAuctionForm(forms.ModelForm):
    value = forms.IntegerField()

    class Meta:
        model = Bid
        fields = ['value']
