from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from core.config import settings  # Import the settings instance

User = get_user_model()


class Command(BaseCommand):
    help = "Create a superuser if one does not exist"

    def handle(self, *args, **kwargs):
        username = settings.superuser.username
        email = settings.superuser.email
        password = settings.superuser.password.get_secret_value()

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(
                username=username, email=email, password=password
            )
            self.stdout.write(
                self.style.SUCCESS(f"Successfully created superuser {username}")
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(f"Superuser {username} already exists")
            )
