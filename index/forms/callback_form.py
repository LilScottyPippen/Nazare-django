from django import forms
from ..models.callback import Callback
from utils.constants import ERROR_MESSAGES
from utils.is_valid_name import is_valid_name
from utils.is_valid_phone import is_valid_phone


class CallbackForm(forms.ModelForm):
    class Meta:
        model = Callback
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        phone = cleaned_data.get('phone')
        is_privacy_policy = cleaned_data.get('is_privacy_policy')

        if not is_valid_name(name):
            raise forms.ValidationError(ERROR_MESSAGES['invalid_name'])

        if not is_privacy_policy or type(is_privacy_policy) != bool:
            raise forms.ValidationError(ERROR_MESSAGES['invalid_privacy_policy'])

        if not is_valid_phone(phone):
            raise forms.ValidationError(ERROR_MESSAGES['invalid_phone'])
