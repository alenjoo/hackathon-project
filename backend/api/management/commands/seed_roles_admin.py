from django.core.management.base import BaseCommand
from api.models import Role, User
from django.contrib.auth.hashers import make_password
import os

class Command(BaseCommand):
    help = 'Seed initial roles and one demo Admin user'

    def handle(self, *args, **kwargs):
        roles = ['Admin', 'Officer', 'Citizen']
        for role_name in roles:
            Role.objects.get_or_create(RoleName=role_name)

        admin_role = Role.objects.get(RoleName='Admin')

        if not User.objects.filter(Email='govadmin@gmail.com').exists():
            salt = os.urandom(32).hex()
            raw_password = '1234567890'
            hashed = make_password(raw_password + salt)

            User.objects.create(
                Name='admin',
                Email='govadmin@gmail.com',
                Mobile='1234567890',
                Salt=salt,
                PasswordHash=hashed,
                Role=admin_role
            )
            self.stdout.write(self.style.SUCCESS('Demo Admin user created.'))
        else:
            self.stdout.write(self.style.WARNING('Admin user already exists.'))

        self.stdout.write(self.style.SUCCESS('Roles seeded successfully.'))
