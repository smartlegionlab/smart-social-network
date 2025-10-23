from django.shortcuts import render

from apps.admin_panel.decorators.superuser import superuser_required
from apps.core.utils.paginator import CachedCountPaginator
from apps.references.models.emoji import Emoji


@superuser_required
def emoji_list_view(request):
    paginate_by = 20

    emoji_list = Emoji.objects.all()
    count = emoji_list.count()
    paginator = CachedCountPaginator(emoji_list, paginate_by, count)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'emoji_list': page_obj,
        'page_obj': page_obj,
        'paginator': paginator,
        'is_exists': emoji_list.exists(),
        'count': count,
    }

    return render(request, 'admin_panel/references/emoji_list.html', context)
