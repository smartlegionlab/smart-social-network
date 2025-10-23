from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MaxLengthValidator, MinValueValidator, MaxValueValidator

from apps.core.utils.checkers.checkers import check_phone_number
from apps.references.models.city import City
from apps.users.models import User


class BaseUserForm(forms.ModelForm):
    about_me = forms.CharField(
        widget=forms.Textarea,
        validators=[MaxLengthValidator(500)],
        required=False,
        label='About Me'
    )
    date_of_birth = forms.DateField(
        label='Date Of Birth',
        widget=forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d',),
        required=False,
    )
    city = forms.ModelChoiceField(
        required=False,
        widget=forms.Select(),
        queryset=City.objects.all(),
        label='City'
    )
    telegram_chat_id = forms.IntegerField(
        required=False,
        label='Telegram Chat ID',
        validators=[
            MinValueValidator(1),
            MaxValueValidator(9999999999999999999)
        ],
        widget=forms.TextInput(attrs={'maxlength': '18'})
    )

    class Meta:
        model = User
        fields = [
            'email',
            'first_name',
            'last_name',
            'gender',
            'about_me',
            'date_of_birth',
            'phone',
            'telegram_chat_id',
            'city',
        ]
        labels = {
            'email': 'Email',
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'gender': 'Gender',
            'telegram_chat_id': 'Telegram Chat ID',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if self.fields[field].required:
                self.fields[field].label += ' *'

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone and not check_phone_number(phone):
            raise ValidationError('The phone number must start with 8 and contain 11 digits.')
        return phone
