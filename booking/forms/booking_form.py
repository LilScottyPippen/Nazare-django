from django import forms
from ..models.booking import Booking
from ..models.guest import Guest
from utils.is_valid_date import *
from utils.is_valid_full_name import *
from utils.is_valid_phone import *


class GuestsForm(forms.ModelForm):
    class Meta:
        model = Guest
        fields = '__all__'


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        check_in_date = cleaned_data.get('check_in_date')
        check_out_date = cleaned_data.get('check_out_date')
        client_name = cleaned_data.get('client_name')
        client_surname = cleaned_data.get('client_surname')
        client_father_name = cleaned_data.get('client_father_name')
        client_number = cleaned_data.get('client_number')

        if not is_valid_date_booking(check_in_date, check_out_date):
            raise forms.ValidationError("Booking date is invalid")

        if not is_valid_full_name(client_name, client_surname, client_father_name):
            raise forms.ValidationError("Full name is invalid")

        if not is_valid_phone(client_number):
            raise forms.ValidationError("Phone number is invalid")
