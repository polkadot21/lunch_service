from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from core.models import Restaurant, Menu, Employee

User = get_user_model()


class Command(BaseCommand):
    help = "Delete initial data for roles, restaurants, and menus"

    def handle(self, *args, **kwargs):
        # Delete menus
        Menu.objects.all().delete()
        self.stdout.write(self.style.SUCCESS("Deleted all menus"))

        # Delete restaurants
        Restaurant.objects.all().delete()
        self.stdout.write(self.style.SUCCESS("Deleted all restaurants"))

        # Delete employees (users created for testing)
        employees = Employee.objects.all()
        for employee in employees:
            employee.user.delete()
            employee.delete()
        self.stdout.write(self.style.SUCCESS("Deleted all employees"))
