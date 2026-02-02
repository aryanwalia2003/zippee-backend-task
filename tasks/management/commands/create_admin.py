from django.core.management.base import BaseCommand
from authentication.models import User
import sys

class Command(BaseCommand):
    help = 'Creates an Admin user'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str)
        parser.add_argument('email', type=str)
        parser.add_argument('password', type=str)

    def handle(self, *args, **kwargs):
        username = kwargs['username']
        email = kwargs['email']
        password = kwargs['password']

        if User.get_by_username(username):
            self.stdout.write(self.style.ERROR(f'User {username} already exists'))
            return
            
        if User.get_by_email(email):
            self.stdout.write(self.style.ERROR(f'Email {email} already exists'))
            return

        User.create(username, email, password, role='admin')
        self.stdout.write(self.style.SUCCESS(f'Successfully created Admin: {username}'))
