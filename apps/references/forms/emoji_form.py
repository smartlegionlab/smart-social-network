from django import forms

from apps.references.models.emoji import Emoji


class EmojiForm(forms.ModelForm):
    class Meta:
        model = Emoji
        fields = ['code', 'description']
