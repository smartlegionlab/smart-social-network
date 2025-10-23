from django import forms

from apps.audio_files.models import AudioFile


class AudioFileForm(forms.ModelForm):
    class Meta:
        model = AudioFile
        fields = ['file', 'title',]
        widgets = {
            'file': forms.ClearableFileInput(attrs={'accept': '.mp3,audio/*'}),
        }

    def clean_audio_file(self):
        audio_file = self.cleaned_data.get('file')
        if audio_file:
            if not audio_file.name.endswith('.mp3'):
                raise forms.ValidationError("The file must be in MP3 format.")
            if audio_file.size > 30 * 1024 * 1024:
                raise forms.ValidationError("The file size must not exceed 30MB.")
        return audio_file
