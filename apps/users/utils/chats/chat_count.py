

def get_chats_count(user):
    return user.chat_participants.filter(is_deleted=False).count()
