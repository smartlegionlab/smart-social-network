from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from apps.core.utils.paginator import CachedCountPaginator
from apps.smart_password_manager.services import SmartPasswordService


@login_required
def smart_password_list_view(request):
    password = request.session.pop('password', None)
    smart_passwords = SmartPasswordService.get_user_smart_passwords(request.user)
    password_count = smart_passwords.count()
    paginator = CachedCountPaginator(smart_passwords, 10, password_count)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'password': password,
        'page_obj': page_obj,
        'active_page': 'apps',
        'password_count': password_count,
        'has_passwords': password_count > 0,
    }
    return render(request, 'smart_password_manager/smart_password_manager.html', context)