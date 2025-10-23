from django.contrib import admin

from apps.friends.models import Friendship, FriendshipHistory

admin.site.register(Friendship)
admin.site.register(FriendshipHistory)
