from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from apps.admin_panel.decorators.superuser import superuser_required
from apps.references.forms.emoji_form import EmojiForm


@superuser_required
def emoji_create_view(request):
    success_url = reverse_lazy('admin_panel:emoji_list')

    if request.method == 'POST':
        form = EmojiForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Emoji created!')
            return redirect(success_url)
    else:
        form = EmojiForm()

    return render(request, 'admin_panel/references/emoji_form.html', {'form': form})
