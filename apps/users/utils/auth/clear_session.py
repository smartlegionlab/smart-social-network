

def clear_session_data(request):
    keys_to_remove = ["user_id", "user_email", "user_password"]
    for key in keys_to_remove:
        request.session.pop(key, None)
