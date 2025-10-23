from django import forms
from django.contrib.auth.forms import PasswordChangeForm

from apps.users.models import User


class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label='Old Password', widget=forms.PasswordInput)
    new_password1 = forms.CharField(label='New Password', widget=forms.TextInput)
    new_password2 = forms.CharField(label='Confirm new password', widget=forms.TextInput)

    class Meta:
        model = User
        fields = ('old_password', 'new_password1', 'new_password2')
