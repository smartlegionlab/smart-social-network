from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MaxLengthValidator

from apps.user_images.models import UserImage


class UserImageForm(forms.ModelForm):
    description = forms.CharField(
        widget=forms.Textarea,
        validators=[MaxLengthValidator(100)],
        required=False
    )

    class Meta:
        model = UserImage
        fields = ['image', 'title', 'description', 'is_visible']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].required = False

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get('title') and cleaned_data.get('image'):
            cleaned_data['title'] = cleaned_data['image'].name
        return cleaned_data

    def clean_image(self):
        image = self.cleaned_data.get('image')

        if not image:
            raise ValidationError('Please upload an image.')

        if not image.name.endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp')):
            raise ValidationError('Acceptable formats: PNG, JPG, JPEG, GIF, WEBP.')

        if image.size > 5 * 1024 * 1024:
            raise ValidationError('The image size must not exceed 5 МБ.')

        return image
