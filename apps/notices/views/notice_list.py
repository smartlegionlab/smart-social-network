from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from apps.core.utils.paginator import CachedCountPaginator
from apps.notices.services import NoticeService


@login_required
def user_notice_list_view(request):
    notices = NoticeService.get_user_notices(request.user)
    notice_count = notices.count()

    paginator = CachedCountPaginator(notices, 10, notice_count)
    page = request.GET.get('page', 1)
    page_obj = paginator.get_page(page)

    context = {
        'page_obj': page_obj,
        'active_page': 'notices',
        'notice_count': notice_count,
        'has_notices': notice_count > 0,
    }
    return render(request, 'notices/notice_list.html', context)
