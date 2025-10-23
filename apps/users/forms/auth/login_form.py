from django import forms


class LoginForm(forms.Form):
    email = forms.EmailField(
        max_length=150,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email'
        }),
        error_messages={'required': 'Email is required!'}
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password'
        }),
        error_messages={'required': 'Password is required!'}
    )
