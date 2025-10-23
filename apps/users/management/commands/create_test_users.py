import datetime

from django.core.management.base import BaseCommand
import random
import string
import uuid

from apps.users.models import User


class Command(BaseCommand):
    help = 'Create test users'

    def add_arguments(self, parser):
        parser.add_argument('count', type=int, help='Number of test users to create')

    def handle(self, *args, **kwargs):
        count = kwargs['count']
        batch_size = 1000
        created_users = []

        for _ in range(count):
            email = f'test_{uuid.uuid4()}@example.com'
            first_name = ''.join(random.choices(string.ascii_letters, k=5))
            last_name = ''.join(random.choices(string.ascii_letters, k=5))

            user = User(
                email=email,
                first_name=first_name,
                last_name=last_name,
                is_test=True,
                date_of_birth=datetime.date.today(),
            )
            created_users.append(user)

            if len(created_users) >= batch_size:
                User.objects.bulk_create(created_users)
                created_users = []

        if created_users:
            User.objects.bulk_create(created_users)

        self.stdout.write(self.style.SUCCESS(f'Successfully created {count} test users.'))
