from django import forms
from ..models.booking import Booking
from ..models.guest import Guest


class GuestsForm(forms.ModelForm):
    class Meta:
        model = Guest
        fields = '__all__'


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = '__all__'
