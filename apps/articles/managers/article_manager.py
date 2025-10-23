from django.db import models
from django.utils import timezone


class ArticleManager(models.Manager):
    def published(self):
        return self.filter(status='published', published_at__lte=timezone.now())

    def drafts(self):
        return self.filter(status='draft')

    def archived(self):
        return self.filter(status='archived')

    def visible(self):
        return self.published()

    def by_author(self, author):
        return self.filter(author=author)
