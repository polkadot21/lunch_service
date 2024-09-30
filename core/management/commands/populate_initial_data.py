from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from core.models import Restaurant, Menu, Employee
from django.utils import timezone

from faker import Faker
import random

User = get_user_model()
fake = Faker()


class Command(BaseCommand):
    help = "Populate initial data for roles, restaurants, and menus, including owners"

    def handle(self, *args, **kwargs):
        # Create a user to act as a restaurant owner
        owner_data = {
            "username": "restaurant_owner",
            "email": "owner@example.com",
            "password": "ownerpass123",
        }
        owner, created = User.objects.get_or_create(
            username=owner_data["username"],
            email=owner_data["email"],
            is_staff=False,
        )
        if created:
            owner.set_password(owner_data["password"])
            owner.save()
            self.stdout.write(
                self.style.SUCCESS(f'Created owner "{owner_data["username"]}"')
            )

        # Create restaurants and assign the owner
        restaurant_data = [
            {
                "name": "The Gourmet Kitchen",
                "address": fake.address(),
                "phone_number": fake.phone_number(),
                "owner": owner,
            },
            {
                "name": "Pasta Palace",
                "address": fake.address(),
                "phone_number": fake.phone_number(),
                "owner": owner,
            },
            {
                "name": "Sushi Central",
                "address": fake.address(),
                "phone_number": fake.phone_number(),
                "owner": owner,
            },
        ]

        restaurants = []
        for data in restaurant_data:
            restaurant, created = Restaurant.objects.get_or_create(
                name=data["name"],
                defaults={
                    "address": data["address"],
                    "phone_number": data["phone_number"],
                    "owner": data["owner"],
                },
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created restaurant "{data["name"]}"')
                )
            restaurants.append(restaurant)

        # Create diverse menus for each restaurant
        today = timezone.now().date()
        menu_items = {
            "The Gourmet Kitchen": [
                "Steak",
                "Roasted Vegetables",
                "Grilled Salmon",
                "Caesar Salad",
                "Garlic Bread",
            ],
            "Pasta Palace": [
                "Spaghetti Bolognese",
                "Penne Arrabbiata",
                "Fettuccine Alfredo",
                "Garlic Bread",
                "Tiramisu",
            ],
            "Sushi Central": [
                "California Roll",
                "Spicy Tuna Roll",
                "Miso Soup",
                "Sashimi Platter",
                "Green Tea Ice Cream",
            ],
        }

        for restaurant in restaurants:
            menu_date = today
            # Create menus for today and for the next 3 days
            for i in range(4):
                menu_items_today = random.sample(menu_items[restaurant.name], k=3)
                Menu.objects.get_or_create(
                    restaurant=restaurant,
                    date=menu_date,
                    defaults={"items": ", ".join(menu_items_today)},
                )
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Created menu for "{restaurant.name}" on {menu_date} with items: {", ".join(menu_items_today)}'
                    )
                )
                menu_date += timezone.timedelta(days=1)

        # Create employees with different roles and departments
        employee_data = [
            {
                "username": "john_doe",
                "email": "john.doe@example.com",
                "password": "securepassword123",
                "department": "Engineering",
            },
            {
                "username": "jane_smith",
                "email": "jane.smith@example.com",
                "password": "securepassword123",
                "department": "Marketing",
            },
            {
                "username": "alice_johnson",
                "email": "alice.johnson@example.com",
                "password": "securepassword123",
                "department": "Sales",
            },
            {
                "username": "bob_brown",
                "email": "bob.brown@example.com",
                "password": "securepassword123",
                "department": "Human Resources",
            },
        ]

        for data in employee_data:
            user, created = User.objects.get_or_create(
                username=data["username"],
                email=data["email"],
                is_staff=False,
            )
            if created:
                user.set_password(data["password"])
                user.save()
                Employee.objects.get_or_create(user=user, department=data["department"])
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Created employee "{data["username"]}" in department "{data["department"]}"'
                    )
                )

        # Output a summary of the populated data
        self.stdout.write(self.style.SUCCESS("\n--- Summary of Initial Data ---"))
        self.stdout.write(
            self.style.SUCCESS(f"Created {len(restaurant_data)} restaurants.")
        )
        self.stdout.write(
            self.style.SUCCESS(f"Created {len(employee_data)} employees.")
        )
        self.stdout.write(
            self.style.SUCCESS("Created menus for the next 4 days for each restaurant.")
        )
