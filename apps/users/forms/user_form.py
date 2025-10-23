from django import forms
from django.core.exceptions import ValidationError

from apps.users.forms.user_base_form import BaseUserForm


class UserEditForm(BaseUserForm):
    class Meta(BaseUserForm.Meta):
        fields = BaseUserForm.Meta.fields + ['is_2fa_enabled', 'username']
        labels = {
            **BaseUserForm.Meta.labels,
            'is_2fa_enabled': 'Two-factor authentication',
        }
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        is_2fa_enabled = cleaned_data.get('is_2fa_enabled')
        telegram_chat_id = cleaned_data.get('telegram_chat_id')

        if is_2fa_enabled and not telegram_chat_id:
            raise ValidationError('You must provide a Telegram Chat ID if two-factor authentication is enabled.')
        return cleaned_data
