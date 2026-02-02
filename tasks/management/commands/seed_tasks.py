from django.core.management.base import BaseCommand
from tasks.models import Task
from authentication.models import User
import uuid
import random

class Command(BaseCommand):
    help = 'Seeds the database with 1000 unique tasks'

    def handle(self, *args, **kwargs):
        self.stdout.write('Starting seeding process...')

        # Ensure we have a user to assign tasks to
        user = User.get_by_username('seed_user')
        if not user:
            user = User.create('seed_user', 'seed@example.com', 'password123')
            self.stdout.write(self.style.SUCCESS('Created test user: seed_user'))
        else:
            self.stdout.write('Using existing user: seed_user')

        user_id = user['id']

        # Generate 1000 tasks
        for i in range(1000):
            unique_id = uuid.uuid4().hex[:8]
            title = f"Task {i+1} - {unique_id}"
            description = f"This is a description for task {i+1}. Generated automatically."
            
            Task.create(title, description, user_id)
            
            if (i + 1) % 100 == 0:
                self.stdout.write(f'Created {i + 1} tasks...')

        self.stdout.write(self.style.SUCCESS('Successfully seeded 1000 tasks!'))
