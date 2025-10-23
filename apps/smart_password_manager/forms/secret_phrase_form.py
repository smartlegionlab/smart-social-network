from django import forms


class SecretPhraseForm(forms.Form):
    secret_phrase = forms.CharField(
        max_length=255,
        label='Secret phrase',
        widget=forms.PasswordInput(attrs={'autocomplete': 'off'})
    )
