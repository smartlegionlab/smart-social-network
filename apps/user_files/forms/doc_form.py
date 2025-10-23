from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MaxLengthValidator

from apps.user_files.models.doc import DocumentFile


class DocFileForm(forms.ModelForm):
    description = forms.CharField(
        widget=forms.Textarea,
        validators=[MaxLengthValidator(100)],
        required=False
    )

    class Meta:
        model = DocumentFile
        fields = ['file', 'title', 'description', 'is_visible']
        widgets = {
            'file': forms.ClearableFileInput(attrs={'accept': '.pdf,.docx,.txt'}),
        }

    def clean_file(self):
        file = self.cleaned_data.get('file')

        if not file:
            raise ValidationError('Please upload the document.')

        if not file.name.endswith(('.pdf', '.doc', '.docx', '.txt')):
            raise ValidationError('Acceptable formats: PDF, DOC, DOCX, TXT.')

        if file.size > 30 * 1024 * 1024:
            raise ValidationError('The document size must not exceed 30 MB.')

        return file


class DocumentFileUpdateForm(forms.ModelForm):
    description = forms.CharField(
        widget=forms.Textarea,
        validators=[MaxLengthValidator(100)],
        required=False
    )

    class Meta:
        model = DocumentFile
        fields = ['title', 'description', 'is_visible']
