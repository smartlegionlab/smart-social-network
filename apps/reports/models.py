from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

class UserReportQuerySet(models.QuerySet):
    def with_related_users(self):
        return self.select_related('reporter', 'reported_user')


class UserReport(models.Model):
    REPORT_REASONS = [
        ('spam', 'Spam or advertising'),
        ('fake_news', 'Fake news'),
        ('misinformation', 'Misinformation'),
        ('scam', 'Scam'),
        ('phishing', 'Phishing'),
        ('hate_speech', 'Hate speech'),
        ('extremism', 'Extremism'),
        ('terrorism', 'Terrorism'),
        ('violence', 'Violence'),
        ('self_harm', 'Self-harm promotion'),
        ('harassment', 'Harassment'),
        ('bullying', 'Bullying'),

        ('threats', 'Threats'),
        ('blackmail', 'Blackmail'),

        ('nudity', 'Nudity'),
        ('pornography', 'Pornography'),
        ('sexual_content', 'Sexual content'),
        ('underage', 'Underage content'),

        ('doxing', 'Doxing'),
        ('private_info', 'Private information leak'),
        ('impersonation', 'Impersonation'),
        ('fake_account', 'Fake account'),

        ('copyright', 'Copyright infringement'),
        ('trademark', 'Trademark violation'),
        ('counterfeit', 'Counterfeit goods'),

        ('illegal_goods', 'Illegal goods'),
        ('drugs', 'Drugs'),
        ('weapons', 'Weapons'),
        ('animal_abuse', 'Animal abuse'),
        ('other', 'Other violation'),
    ]

    REPORT_STATUSES = [
        ('submitted', 'Report submitted'),
        ('in_progress', 'Under review'),
        ('resolved', 'Report approved'),
        ('rejected', 'Report rejected'),
        ('closed', 'Report closed'),
    ]

    reporter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='filed_reports'
    )
    reported_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reports_against'
    )
    reason = models.CharField(max_length=50, choices=REPORT_REASONS)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=15,
        choices=REPORT_STATUSES,
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_reports'
    )
    image = models.ImageField(
        upload_to='reports/%Y/%m/%d/',
        blank=True,
        null=True
    )
    objects = UserReportQuerySet.as_manager()

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return f"Report #{self.id} on {self.reported_user} ({self.get_status_display()})"

    def clean(self):
        if not self.image:
            raise ValidationError("Image proof is required for submission!")
