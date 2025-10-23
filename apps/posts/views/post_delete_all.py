from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.shortcuts import redirect

from apps.posts.services import PostService


@login_required
def post_delete_all_view(request):
    try:
        deleted_count = PostService.delete_all_user_posts(request.user)
        messages.success(request, 'The wall was cleared.')
    except ValidationError as e:
        messages.error(request, e.messages[0])
    except Exception as e:
        print(e)
        messages.error(request, 'Something went wrong.')
    return redirect('users:current_user')
