from typing import Any

from django.contrib.auth.models import User, Permission
from django.core.management.base import BaseCommand, CommandError, CommandParser


class Command(BaseCommand):
    help = "Creates a user and give the CRUD permissions"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("username", type=str)
        parser.add_argument("password", type=str, default=None)

    def handle(self, *args: Any, **options: Any) -> None:
        username = options["username"]
        password = options.get("password")

        if not password:
            password = input(f"Enter the password for the user '{username}': ")

        if len(password) < 8:
            raise CommandError("Please enter a password longer than 8 characters.")
        user = User.objects.create_user(username, password=password)
        user.user_permissions.add(
            *Permission.objects.filter(codename__iendswith="_jiramapping")
        )
        self.stdout.write(
            self.style.SUCCESS(f"Successfully created user '{user.username}'")
        )
