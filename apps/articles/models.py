from math import ceil

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from tinymce.models import HTMLField

from apps.articles.managers.article_manager import ArticleManager
from apps.core.models.abstract_models import AbstractLike
from apps.core.models.mixins import LikeableMixin
from apps.core.utils.translate import transliterate_cyrillic


class Article(LikeableMixin, models.Model):
    STYLE_CHOICES = [
        ('primary', 'Primary'),
        ('danger', 'Danger'),
        ('warning', 'Warning'),
        ('success', 'Success'),
        ('secondary', 'Secondary'),
    ]

    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    image = models.ImageField(upload_to='articles/%Y/%m/%d/', blank=True, null=True)
    content = HTMLField(default='')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(blank=True, null=True)

    readers = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='read_articles',
        blank=True
    )

    style_class = models.CharField(
        max_length=20,
        choices=STYLE_CHOICES,
        default='primary'
    )
    total_views = models.PositiveIntegerField(default=0)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft'
    )

    objects = ArticleManager()

    class Meta:
        ordering = ('-published_at', '-created_at')
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'
        indexes = [
            models.Index(fields=['-published_at']),
            models.Index(fields=['status']),
            models.Index(fields=['slug']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        if self.image:
            self.image.delete(save=False)
        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        if not self.slug:
            super().save(*args, **kwargs)
            base_slug = slugify(transliterate_cyrillic(self.title))
            self.slug = f"{base_slug}-{self.id}"

        if self.status == 'published':
            self.published_at = timezone.now()

        super().save(*args, **kwargs)

    def publish(self):
        self.status = 'published'
        self.save()

    def unpublish(self):
        self.status = 'draft'
        self.save()

    def archive(self):
        self.status = 'archived'
        self.save()

    @property
    def is_published(self):
        return (self.status == 'published' and
                self.published_at is not None and
                self.published_at <= timezone.now())

    @property
    def reading_time(self):
        words_per_minute = 200

        word_count = len(self.content.strip().split())

        minutes = ceil(word_count / words_per_minute)

        if minutes < 1:
            return "less than a minute"
        elif minutes == 1:
            return "1 minute"
        elif minutes < 60:
            return f"{minutes} minutes"

        hours = minutes // 60
        remaining_minutes = minutes % 60

        if hours == 1:
            if remaining_minutes == 0:
                return "1 hour"
            else:
                return f"1 hour {remaining_minutes} minutes"
        else:
            if remaining_minutes == 0:
                return f"{hours} hours"
            else:
                return f"{hours} hours {remaining_minutes} minutes"

    def increment_views(self):
        self.total_views += 1
        self.save(update_fields=['total_views'])

    def get_absolute_url(self):
        return reverse('articles:article_detail', kwargs={'slug': self.slug})


class ArticleLike(AbstractLike):
    article = models.ForeignKey(
        'Article',
        on_delete=models.CASCADE,
        related_name='likes'
    )

    class Meta:
        unique_together = ('user', 'article')
        verbose_name = 'Article Like'
        verbose_name_plural = 'Article Likes'
        indexes = [
            models.Index(fields=['article', 'user']),
            models.Index(fields=['user', 'article']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"{self.user} → post #{self.article.id}"


class ArticleComment(LikeableMixin, models.Model):
    article = models.ForeignKey(
        'Article',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='authored_article_comments',
        db_index=True
    )
    content = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    is_edit = models.BooleanField(default=False)
    edited_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Article Comment'
        verbose_name_plural = 'Article Comments'

    def __str__(self):
        return f"{self.author.full_name} commented post #{self.article.id}"


class ArticleCommentLike(AbstractLike):
    comment = models.ForeignKey(
        'ArticleComment',
        on_delete=models.CASCADE,
        related_name='likes'
    )

    class Meta:
        unique_together = ('user', 'comment')
        verbose_name = 'Article Comment Like'
        verbose_name_plural = 'Article Comment Likes'

        indexes = [
            models.Index(fields=['comment', 'user']),
            models.Index(fields=['user', 'comment']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"{self.user} → comment #{self.comment.id}"
