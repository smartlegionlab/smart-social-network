from django.urls import path

from apps.friends.views.friend_delete import friend_delete_view
from apps.friends.views.friend_list import friend_list_view
from apps.friends.views.friend_requests.friend_request_accept import friend_request_accept_view
from apps.friends.views.friend_requests.friend_request_cancel import friend_request_cancel_view
from apps.friends.views.friend_requests.friend_request_reject import friend_request_reject_view
from apps.friends.views.friend_requests.friend_request_send import friend_request_send_view
from apps.friends.views.friend_requests.incoming_request_list import incoming_request_list_view
from apps.friends.views.friend_requests.outgoing_request_list import outgoing_request_list_view

app_name = 'friends'

urlpatterns = [
    path('', friend_list_view, name='friend_list'),
    path('requests/send/<int:user_id>/', friend_request_send_view, name='friend_request_send'),
    path('requests/accept/<int:friendship_id>/', friend_request_accept_view, name='friend_request_accept'),
    path('requests/reject/<int:friendship_id>/', friend_request_reject_view, name='friend_request_reject'),
    path('requests/cancel/<int:friendship_id>/', friend_request_cancel_view, name='friend_request_cancel'),
    path('delete/<int:user_id>/', friend_delete_view, name='friend_delete'),
    path('requests/incoming/', incoming_request_list_view, name='incoming_request_list'),
    path('requests/outgoing/', outgoing_request_list_view, name='outgoing_request_list'),
    path('@<str:username>/', friend_list_view, name='public_user_friends'),
]
