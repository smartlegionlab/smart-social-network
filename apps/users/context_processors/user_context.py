from django.contrib.auth import get_user_model


def user_context_processor(request):
    User = get_user_model()

    context = {
        'current_user': request.user if request.user.is_authenticated else None,
        'public_user': None,
        'profile': None,
        'is_owner': False
    }

    if not context['current_user']:
        return context

    kwargs = request.resolver_match.kwargs

    user_queryset = User.objects.only(
            'id', 'username', 'first_name', 'last_name', 'avatar',
            'city_id', 'is_active', 'created_at', 'city__name',
            'last_activity', 'gender', 'about_me', 'date_of_birth',
            'email', 'phone', 'telegram_chat_id', 'is_2fa_enabled', 'updated_at'
        ).filter(is_active=True)

    try:
        if 'username' in kwargs:
            context['public_user'] = user_queryset.get(username=kwargs['username'])
        elif 'user_id' in kwargs:
            context['public_user'] = user_queryset.get(id=kwargs['user_id'])
        else:
            context['public_user'] = context['current_user']
            context['is_owner'] = True
    except User.DoesNotExist:
        context['public_user'] = context['current_user']
        context['is_owner'] = True

    context['profile'] = context['public_user']
    context['is_owner'] = (context['current_user'].id == context['public_user'].id)

    return context
