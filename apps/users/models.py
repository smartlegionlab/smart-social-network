from datetime import timedelta

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.cache import cache
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.db import models
from django.templatetags.static import static
from django.utils import timezone

from django.conf import settings
from django.utils.functional import cached_property

from apps.users.managers.custom_user import CustomUserManager
from apps.users.utils.chats.chat_count import get_chats_count
from apps.users.utils.friends.incoming_requests import get_incoming_requests
from apps.users.utils.friends.outgoing_requests import get_outgoing_requests
from apps.users.utils.friends.user_friend_list import get_user_friends
from apps.users.utils.validators.age import calculate_age

from apps.users.utils.files.avatar_upload_path import avatar_upload_to
from apps.references.models.city import City

LANGUAGES = settings.LANGUAGES


class User(AbstractBaseUser, PermissionsMixin):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    email = models.EmailField(unique=True, db_index=True)
    first_name = models.CharField(max_length=30, db_index=True)
    last_name = models.CharField(max_length=30, db_index=True)
    username = models.CharField(
        verbose_name='username',
        max_length=150,
        unique=True,
        db_index=True,
        null=True,
        blank=True,
        validators=[RegexValidator(
            r'^[a-z][a-z0-9]*$',
            message='Username can only contain lowercase letters and numbers...'
        )]
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    date_of_birth = models.DateField(verbose_name='Date of Birth', null=True, blank=True)
    phone = models.CharField(max_length=11, blank=True, verbose_name='Phone Number', null=True)
    avatar = models.ImageField(
        upload_to=avatar_upload_to,
        blank=True,
        null=True
    )
    last_activity = models.DateTimeField(default=timezone.now)
    language = models.CharField(max_length=10, choices=LANGUAGES, default='en')
    about_me = models.TextField(default='', blank=True)
    is_test = models.BooleanField(default=False)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='O', blank=True, null=True)
    telegram_chat_id = models.BigIntegerField(
        blank=True,
        null=True,
        verbose_name='Telegram Chat ID',
        validators=[
            MinValueValidator(1),
            MaxValueValidator(9999999999999999999)
        ]
    )
    is_2fa_enabled = models.BooleanField(default=False)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, blank=True,
                             null=True, verbose_name='City', related_name='users')
    objects = CustomUserManager()
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def get_avatar_url(self):
        if self.avatar and hasattr(self.avatar, 'url'):
            return self.avatar.url
        return static('users/images/default_avatar.png')

    def toggle_2fa(self):
        self.is_2fa_enabled = not self.is_2fa_enabled
        self.save()

    @property
    def age(self):
        return calculate_age(self.date_of_birth)

    @property
    def age_with_suffix(self):
        age = self.age
        if age is None:
            return None
        elif age == 1:
            return f"{age} year"
        else:
            return f"{age} years"

    @property
    def friends(self):
        return get_user_friends(self)

    @property
    def incoming_requests(self):
        return get_incoming_requests(self)

    @property
    def incoming_requests_count(self):
        return self.incoming_requests.count()

    @property
    def outgoing_requests(self):
        return get_outgoing_requests(self)

    @property
    def outgoing_requests_count(self):
        return self.outgoing_requests.count()

    @property
    def friend_count(self):
        return self.friends.count()

    @property
    def is_online(self):
        last_active = cache.get(f'user_{self.id}_last_activity')

        if last_active is None:
            last_active = self.last_activity

        if last_active is None:
            return False

        return timezone.now() - last_active < timedelta(minutes=5)

    @cached_property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @cached_property
    def optimized_city(self):
        return self.city

    class Meta:
        db_table = 'users_user'
        ordering = ['-created_at']

        indexes = [
            models.Index(fields=['first_name'], name='first_name_idx'),
            models.Index(fields=['last_name'], name='last_name_idx'),
            models.Index(fields=['username'], name='username_idx'),

            models.Index(fields=['first_name', 'last_name'], name='first_last_name_idx'),
        ]

    def switch_activity(self):
        self.is_active = not self.is_active
        self.save()

    def avatar_upload_to(self, filename):
        return f"avatars/{self.id}/{filename}"

    @property
    def chats_count(self):
        return get_chats_count(self)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if not self.username:
            self.username = f"user{self.id}"
            self.save(update_fields=['username'])

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
