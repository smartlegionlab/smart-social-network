from django import forms
from django.core.validators import MaxLengthValidator
from apps.reports.models import UserReport


class UserReportForm(forms.ModelForm):
    description = forms.CharField(
        widget=forms.Textarea,
        validators=[MaxLengthValidator(3000)],
        required=False
    )

    class Meta:
        model = UserReport
        fields = ['reason', 'description', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['description'].required = True

        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
            if self.fields[field].required:
                self.fields[field].label_suffix = ''

        self.fields['image'].widget.attrs.update({
            'accept': 'image/*',
            'class': 'form-control form-control-lg'
        })

    def clean(self):
        cleaned_data = super().clean()
        if 'image' not in self.files:
            self.add_error('image', "Image proof is required for submission!")
        return cleaned_data

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            if image.size > 5 * 1024 * 1024:
                raise forms.ValidationError("Image file too large ( > 5MB )")
            if not image.content_type.startswith('image/'):
                raise forms.ValidationError("File is not an image")
        return image
