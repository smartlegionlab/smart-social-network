from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def app_list_view(request):
    context = {
        'active_page': 'apps',
    }
    return render(request, 'app_hub/app_list.html', context)
