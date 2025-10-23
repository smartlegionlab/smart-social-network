from django.contrib import admin

from apps.auth_logs.models import UserAuthLog

admin.site.register(UserAuthLog)
