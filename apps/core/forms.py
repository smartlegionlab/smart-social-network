from django import forms
from django.core.exceptions import ValidationError

from apps.core.models.site_config import SiteConfig
from apps.core.utils.checkers.checkers import check_phone_number


class SiteConfigForm(forms.ModelForm):
    class Meta:
        model = SiteConfig
        fields = ['name', 'description', 'email', 'phone', 'telegram_bot_token', 'telegram_bot_url']
        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Enter the name of the application'}),
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Enter a description'}),
        }
        labels = {
            'name': 'Application name',
            'description': 'Description of the application',
            'email': 'Email address',
            'phone': 'Phone number',
            'telegram_bot_token': 'Telegram bot token',
            'telegram_bot_url': 'Telegram bot url',
        }

    def __init__(self, *args, **kwargs):
        super(SiteConfigForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if self.fields[field_name].required:
                self.fields[field_name].label += ' *'

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone and not check_phone_number(phone):
            raise ValidationError('The phone number must start with 8 and contain 11 digits.')
        return phone
