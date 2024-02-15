from django import forms

from utils.is_valid_phone import is_valid_phone
from ..models.callback import Callback


class CallbackForm(forms.ModelForm):
    class Meta:
        model = Callback
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        phone = cleaned_data.get('phone')
        is_privacy_policy = cleaned_data.get('is_privacy_policy')

        if not name:
            raise forms.ValidationError("Name is invalid")
        if not name.isalpha():
            raise forms.ValidationError("Name is invalid")
        if len(name) < 2:
            raise forms.ValidationError("Name is invalid")

        if is_privacy_policy is False:
            raise forms.ValidationError("Privacy policy is invalid")

        if not is_valid_phone(phone):
            raise forms.ValidationError("Phone number is invalid")
