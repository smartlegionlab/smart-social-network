from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from apps.posts.views.post_api import PostView
from .views.auth.login import login_view
from .views.auth.logout import logout_view
from apps.users.views.user.password.password_change import password_change_view
from apps.users.views.user.password.password_generate import password_generate_view
from apps.users.views.user.password.password_reset import password_reset_view
from .views.auth.register import register_view
from .views.auth.two_factor import auth_2fa_view, auth_2fa_check_code
from apps.users.views.user.avatar.avatar_reset import user_avatar_reset_view
from apps.users.views.user.avatar.avatar_upload import user_avatar_upload_view
from apps.users.views.api.v1.public_profile_list import UserPublicListView
from apps.users.views.user.user_detail import user_detail_view
from apps.users.views.user.user_delete import user_delete_view
from apps.users.views.user.user_update import user_update_view
from .views.user.user_search import user_search

app_name = 'users'

# User
urlpatterns = [
    path('profile/@<str:username>/', user_detail_view, name='user_detail'),
    path('', user_detail_view, name='current_user'),
    path('delete/', user_delete_view, name='user_delete'),
    path('search/', user_search, name='users_search'),
    path('update/', user_update_view, name='user_update'),
    path('avatar/reset/', user_avatar_reset_view, name='avatar_reset'),
    path('avatar/upload/', user_avatar_upload_view, name='avatar_upload'),
]

# Auth
urlpatterns += [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
    path('auth-2fa/<str:token>/', auth_2fa_view, name='auth_2fa'),
    path('auth-2fa/check/code/', auth_2fa_check_code, name='auth_2fa_check_code'),
    path('password/reset/', password_reset_view, name='password_reset'),
    path('password/change/', password_change_view, name='password_change'),
    path('password/generate/', password_generate_view, name='password_generate'),
]

# API
urlpatterns += [
    path('api/public/users/', UserPublicListView.as_view(), name='api_public_user_list'),
    path('api/posts/<int:user_id>/', PostView.as_view(), name='api_post_list'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
