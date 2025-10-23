from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy

from apps.admin_panel.decorators.superuser import superuser_required
from apps.references.forms.emoji_form import EmojiForm
from apps.references.models.emoji import Emoji


@superuser_required
def emoji_update_view(request, pk):
    success_url = reverse_lazy('admin_panel:emoji_list')

    emoji = get_object_or_404(Emoji, pk=pk)

    if request.method == 'POST':
        form = EmojiForm(request.POST, request.FILES, instance=emoji)
        if form.is_valid():
            form.save()
            messages.success(request, 'Emoji updated!')
            return redirect(success_url)
    else:
        form = EmojiForm(instance=emoji)

    return render(request, 'admin_panel/references/emoji_form.html', {'form': form, 'emoji': emoji})
