from django import forms

from apps.user_images.models import UserImageComment


class ImageCommentForm(forms.ModelForm):
    class Meta:
        model = UserImageComment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Your comment...'
            }),
        }
