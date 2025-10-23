from django.core.validators import RegexValidator


def validate_username(value):
    validator = RegexValidator(
        r'^[a-z][a-z0-9]*$',
        message='Username can only contain lowercase letters and numbers...'
    )
    validator(value)
