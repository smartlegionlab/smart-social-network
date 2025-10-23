from django.contrib import messages
from django.shortcuts import redirect

from apps.admin_panel.decorators.superuser import superuser_required
from apps.references.models.emoji import Emoji


@superuser_required
def emojis_clear_view(request):
    Emoji.objects.all().delete()
    messages.success(request, 'Emoji deleted!')
    return redirect('admin_panel:emoji_list')
