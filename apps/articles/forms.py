from django import forms
from tinymce.widgets import TinyMCE
from django.utils import timezone

from apps.articles.models import Article, ArticleComment


class ArticleForm(forms.ModelForm):
    published_at = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local',
            'class': 'form-control'
        }),
        input_formats=['%Y-%m-%dT%H:%M']
    )

    class Meta:
        model = Article
        fields = [
            'title',
            'image',
            'content',
            'style_class',
            'status',
            'published_at',
        ]
        widgets = {
            'content': TinyMCE(attrs={'cols': 80, 'rows': 30}),
            'style_class': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            if not isinstance(self.fields[field].widget, (forms.CheckboxInput, forms.Select)):
                self.fields[field].widget.attrs.update({'class': 'form-control'})
            if self.fields[field].required:
                self.fields[field].label += ' *'

    def clean(self):
        cleaned_data = super().clean()
        published_at = cleaned_data.get('published_at')

        if published_at and published_at > timezone.now():
            cleaned_data['published_at'] = timezone.now()

        return cleaned_data



class ArticleCommentForm(forms.ModelForm):
    class Meta:
        model = ArticleComment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Write a comment...',
                'maxlength': '255',
            }),
        }
