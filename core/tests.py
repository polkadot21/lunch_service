# Create your tests here.

import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from core.models import Restaurant, Menu, Employee, Vote
from datetime import date


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def create_admin_user():
    user = User.objects.create_superuser(
        username="adminuser", password="adminpass", email="admin@example.com"
    )
    return user


@pytest.fixture
def create_restaurant_user():
    user = User.objects.create_user(username="restaurantuser", password="restpass")
    return user


@pytest.fixture
def create_restaurant(create_restaurant_user):
    return Restaurant.objects.create(
        name="Test Restaurant",
        address="123 Main St",
        phone_number="1234567890",
        owner=create_restaurant_user,  # Assign the owner here
    )


@pytest.fixture
def create_user():
    user = User.objects.create_user(username="testuser", password="testpass")
    return user


@pytest.fixture
def create_employee(create_user):
    employee = Employee.objects.create(user=create_user, department="IT")
    return employee


@pytest.fixture
def create_menu(create_restaurant):
    return Menu.objects.create(
        restaurant=create_restaurant,
        date=date.today(),
        items={"dish1": "description1", "dish2": "description2"},
    )


@pytest.mark.django_db
def test_create_restaurant(api_client, create_admin_user):
    api_client.login(username="adminuser", password="adminpass")
    data = {
        "name": "New Restaurant",
        "address": "456 Elm St",
        "phone_number": "9876543210",
    }
    response = api_client.post("/api/restaurants/", data)
    assert response.status_code == 201
    assert response.data["name"] == "New Restaurant"


@pytest.mark.django_db
def test_create_restaurant_unauthorized(api_client, create_user):
    api_client.login(username="testuser", password="testpass")
    data = {
        "name": "Unauthorized Restaurant",
        "address": "456 Elm St",
        "phone_number": "9876543210",
    }
    response = api_client.post("/api/restaurants/", data)
    assert (
        response.status_code == 403
    )  # Unauthorized user should not be able to create a restaurant


@pytest.mark.django_db
def test_upload_menu(api_client, create_restaurant_user, create_restaurant):
    api_client.login(username="restaurantuser", password="restpass")
    data = {
        "restaurant": create_restaurant.id,
        "date": str(date.today()),
        "items": {"dish1": "Soup", "dish2": "Salad"},
    }
    response = api_client.post("/api/menus/", data, format="json")
    assert response.status_code == 201
    assert response.data["restaurant"] == create_restaurant.id


@pytest.mark.django_db
def test_get_current_day_menu(api_client, create_employee, create_menu):
    api_client.login(username="testuser", password="testpass")
    response = api_client.get("/api/menus/today/")
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["restaurant"] == create_menu.restaurant.id


@pytest.mark.django_db
def test_employee_creation(api_client, create_admin_user, create_user):
    api_client.login(username="adminuser", password="adminpass")
    data = {"user": create_user.id, "department": "HR"}
    response = api_client.post("/api/employees/", data, format="json")
    assert response.status_code == 201
    assert response.data["department"] == "HR"


@pytest.mark.django_db
def test_employee_creation_unauthorized(api_client, create_user):
    api_client.login(username="testuser", password="testpass")
    data = {"user": create_user.id, "department": "HR"}
    response = api_client.post("/api/employees/", data, format="json")
    assert (
        response.status_code == 403
    )  # Unauthorized user should not be able to create an employee


@pytest.mark.django_db
def test_vote_for_menu_old_version(api_client, create_employee, create_menu):
    api_client.login(username="testuser", password="testpass")
    headers = {"HTTP_Build_Version": "1"}
    data = {
        "menu_id": create_menu.id
    }  # Ensure 'menu_id' matches the expected field name
    response = api_client.post("/api/votes/", data, **headers)
    assert response.status_code == 201
    assert Vote.objects.filter(employee=create_employee, menu=create_menu).exists()


@pytest.mark.django_db
def test_vote_for_menu_new_version(api_client, create_employee, create_menu):
    api_client.login(username="testuser", password="testpass")
    headers = {"HTTP_Build_Version": "2"}
    data = {"votes": [{"menu_id": create_menu.id, "points": 3}]}
    response = api_client.post("/api/votes/", data, format="json", **headers)
    assert response.status_code == 201
    assert Vote.objects.filter(
        employee=create_employee, menu=create_menu, points=3
    ).exists()


@pytest.mark.django_db
def test_get_results_for_current_day(
    api_client, create_admin_user, create_employee, create_menu
):
    api_client.login(username="adminuser", password="adminpass")
    # Create a vote for the menu to ensure data exists
    Vote.objects.create(employee=create_employee, menu=create_menu, points=1)

    response = api_client.get("/api/votes/results/today/")
    assert response.status_code == 200
    assert len(response.data) > 0  # Ensure results are returned


@pytest.mark.django_db
def test_get_results_for_current_day_unauthorized(
    api_client, create_employee, create_menu
):
    api_client.login(username="testuser", password="testpass")
    # Unauthorized employee should not be able to view the voting results
    response = api_client.get("/api/votes/results/today/")
    assert response.status_code == 403
