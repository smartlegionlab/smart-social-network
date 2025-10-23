from django import forms

from apps.posts.models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control post-content',
                'rows': 3,
                'placeholder': "What's new with you?"
            }),
        }
