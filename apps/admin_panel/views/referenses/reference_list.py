from django.shortcuts import render

from apps.admin_panel.decorators.superuser import superuser_required
from apps.references.models.city import City
from apps.references.models.emoji import Emoji


@superuser_required
def reference_list_view(request):
    emojis = Emoji.objects.all()
    cities = City.objects.all()
    context = {
        'emoji_list': emojis,
        'city_list': cities,
    }
    return render(request, 'admin_panel/references/reference_list.html', context)
