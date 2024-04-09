from django import forms
from utils.constants import ERROR_MESSAGES
from ..models.booking import Booking
from ..models.guest import Guest, CITIZENSHIP_CHOICES
from utils.is_valid_date import is_valid_date_booking
from utils.is_valid_full_name import is_valid_full_name
from utils.is_valid_phone import is_valid_phone


class GuestsForm(forms.ModelForm):
    class Meta:
        model = Guest
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        guest_name = cleaned_data.get("guest_name")
        guest_surname = cleaned_data.get("guest_surname")
        guest_father_name = cleaned_data.get("guest_father_name")
        guest_citizenship = cleaned_data.get("citizenship")

        if guest_father_name:
            if not is_valid_full_name(guest_name, guest_surname, guest_father_name):
                raise forms.ValidationError(ERROR_MESSAGES['invalid_full_name'])
        else:
            if not is_valid_full_name(guest_name, guest_surname):
                raise forms.ValidationError(ERROR_MESSAGES['invalid_full_name'])

        if guest_citizenship not in [choice[0] for choice in CITIZENSHIP_CHOICES]:
            raise forms.ValidationError(ERROR_MESSAGES['invalid_citizenship'])


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
        client_phone = cleaned_data.get('client_phone')

        if not is_valid_date_booking(check_in_date, check_out_date):
            raise forms.ValidationError(ERROR_MESSAGES['unavailable_period'])

        if client_father_name:
            if not is_valid_full_name(client_name, client_surname, client_father_name):
                raise forms.ValidationError(ERROR_MESSAGES['invalid_full_name'])
        else:
            if not is_valid_full_name(client_name, client_surname):
                raise forms.ValidationError(ERROR_MESSAGES['invalid_full_name'])

        if not is_valid_phone(client_phone):
            raise forms.ValidationError(ERROR_MESSAGES['invalid_phone'])
