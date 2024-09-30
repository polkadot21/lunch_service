from django.db import models

# Create your models here.
from django.contrib.auth.models import User


class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    phone_number = models.CharField(max_length=50)
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="restaurants",
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name


class Menu(models.Model):
    restaurant = models.ForeignKey(
        Restaurant, related_name="menus", on_delete=models.CASCADE
    )
    date = models.DateField()
    items = models.JSONField()  # Store menu items as a JSON object

    def __str__(self):
        return f"{self.restaurant.name} - {self.date}"


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.CharField(max_length=255)

    def __str__(self):
        return self.user.username


class Vote(models.Model):
    employee = models.ForeignKey(
        Employee, related_name="votes", on_delete=models.CASCADE
    )
    menu = models.ForeignKey(Menu, related_name="votes", on_delete=models.CASCADE)
    points = models.PositiveIntegerField(
        default=1
    )  # Accepts points between 1 to 3 for new versions

    class Meta:
        unique_together = (
            "employee",
            "menu",
        )  # Ensure each employee can vote only once per menu
