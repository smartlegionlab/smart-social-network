from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404

from apps.admin_panel.decorators.superuser import superuser_required
from apps.references.models.emoji import Emoji


@superuser_required
def emoji_delete_view(request, pk):
    emoji = get_object_or_404(Emoji, pk=pk)
    emoji.delete()
    messages.success(request, 'Emoji deleted!')
    return redirect('admin_panel:emoji_list')
