from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from apps.chats.models.chat import ChatStatus
from apps.chats.services.chat_service import ChatService
from apps.users.models import User


@login_required
def start_private_chat_view(request, user_id):
    recipient = get_object_or_404(User, id=user_id)

    if recipient == request.user:
        messages.error(request, "You can't create a chat with yourself")
        return redirect('chats:active_chat_list')

    chat = ChatService.get_or_create_private_chat(request.user, recipient)

    recipient_status = ChatStatus.objects.filter(
        Q(chat__participants=recipient) &
        Q(chat__participants=request.user),
        chat__is_group=False,
        user=recipient
    ).first()

    if recipient_status and not recipient_status.is_visible:
        recipient_status.is_visible = True
        recipient_status.save()

    return redirect('chats:chat_detail', chat_id=chat.id)


@login_required
def chat_create_view(request):
    if request.method == 'POST':
        participant_ids = request.POST.getlist('participants')
        name = request.POST.get('name', '').strip()

        if not participant_ids:
            messages.error(request, 'Please select at least one participant')
            return redirect('chats:chat_create')

        participants = User.objects.filter(id__in=participant_ids)

        if len(participants) == 1:
            return start_private_chat_view(request, participants.first().id)
        else:
            chat = ChatService.create_group_chat(
                creator=request.user,
                participants=[request.user] + list(participants),
                name=name or None
            )
            if chat.name is None:
                chat.name = 'Group Chat #{0}'.format(chat.id)
                chat.save()
            messages.success(request, 'Group chat created successfully')
            return redirect('chats:chat_detail', chat_id=chat.id)

    friends = request.user.friends.all()
    return render(request, 'chats/create_chat.html', {
        'users': friends,
        'is_group_creation': True,
        'active_page': 'chats'
    })
