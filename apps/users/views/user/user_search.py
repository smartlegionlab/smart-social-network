from django.contrib.auth.decorators import login_required
from django.db.models import Value, Q
from django.db.models.functions import Concat
from django.shortcuts import render
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.core.paginator import Paginator

from apps.users.models import User


@login_required
def user_search(request):
    query = request.GET.get('q', '').strip()
    users = []

    if query:
        users = User.objects.annotate(
            full_name_search=Concat('first_name', Value(' '), 'last_name')
        ).filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(username__icontains=query) |
            Q(full_name_search__icontains=query)
        ).order_by('first_name', 'last_name').distinct()

    paginator = Paginator(users, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        html = render_to_string('users/partials/user_search_results.html', {
            'users': page_obj,
            'query': query
        }, request)
        return JsonResponse({'html': html})

    return render(request, 'users/user/search_users.html', {
        'users': page_obj,
        'query': query,
        'active_page': 'search',
    })
