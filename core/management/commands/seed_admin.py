import os
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Seeds the initial admin superuser idempotently from environment variables.'

    def handle(self, *args, **options):
        # Fall back to default development credentials if variables are missing
        username = os.environ.get('ADMIN_USERNAME', 'admin')
        email = os.environ.get('ADMIN_EMAIL', 'admin@gmail.com')
        password = os.environ.get('ADMIN_PASSWORD', 'admin123')

        # 🌟 Idempotency Check: Verify if the user already exists
        if not User.objects.filter(username=username).exists():
            self.stdout.write("Seeding process: Creating initial administrator account...")
            
            # Using create_superuser ensures the password gets properly hashed
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            self.stdout.write(self.style.SUCCESS(f"Successfully seeded admin account: '{username}'"))
        else:
            self.stdout.write(self.style.WARNING(f"Admin seed skipped: User '{username}' already exists in database."))