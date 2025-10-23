from django.core.management.base import BaseCommand

from apps.users.models import User


class Command(BaseCommand):
    help = 'Delete all test users'

    def handle(self, *args, **kwargs):
        test_users = User.objects.filter(is_test=True)
        count = test_users.count()

        test_users.delete()

        self.stdout.write(self.style.SUCCESS(f'Successfully deleted {count} test users.'))
