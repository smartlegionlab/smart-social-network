from django.contrib.auth.models import BaseUserManager

from django.conf import settings
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.db.models import QuerySet

LANGUAGES = settings.LANGUAGES

class UserQuerySet(QuerySet):
    def search(self, query):
        search_vector = SearchVector('first_name', 'last_name', 'username')
        search_query = SearchQuery(query)
        return self.annotate(
            search=search_vector,
            rank=SearchRank(search_vector, search_query)
        ).filter(search=search_query).order_by('-rank')


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email address is required.")

        email = self.normalize_email(email)

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self.create_user(email, password, **extra_fields)

    def get_queryset(self):
        return UserQuerySet(self.model, using=self._db)

    def search(self, query):
        return self.get_queryset().search(query)
