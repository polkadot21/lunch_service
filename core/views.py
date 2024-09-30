from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .models import Restaurant, Menu, Employee, Vote
from .serializers import (
    RestaurantSerializer,
    MenuSerializer,
    EmployeeSerializer,
    VoteSerializer,
)
from .permissions import (
    IsAdmin,
    IsEmployee,
    ReadOnly,
    IsVoteOwner,
    IsRestaurantOwner,
)
from rest_framework.exceptions import ValidationError, PermissionDenied

V2: int = 2


class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        """Grant permission to admin for creating, updating, and deleting restaurants."""
        if self.action in ["create", "update", "partial_update", "destroy"]:
            self.permission_classes = [IsAdmin]
        else:
            self.permission_classes = [IsAuthenticated | ReadOnly]
        return super().get_permissions()


class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            self.permission_classes = [IsAuthenticated, IsRestaurantOwner]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def perform_create(self, serializer):
        # Ensure the restaurant in the request belongs to the authenticated user
        restaurant = serializer.validated_data["restaurant"]
        if restaurant.owner != self.request.user:
            raise PermissionDenied(
                "You do not have permission to add a menu for this restaurant."
            )
        serializer.save()

    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    def today(self, request):
        today = timezone.now().date()
        menus = Menu.objects.filter(date=today)
        serializer = self.get_serializer(menus, many=True)
        return Response(serializer.data)


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAdmin]  # Only admin can manage employee data


class VoteViewSet(viewsets.ModelViewSet):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer

    def get_serializer_class(self):
        """Return different serializers based on build version in the request."""
        return VoteSerializer

    def get_permissions(self):
        """Set custom permissions for different actions."""
        if self.action in ["update", "partial_update", "destroy"]:
            self.permission_classes = [IsAuthenticated, IsVoteOwner]
        elif self.action == "create":
            self.permission_classes = [IsAuthenticated, IsEmployee]
        elif self.action == "get_today_results":
            self.permission_classes = [IsAuthenticated, IsAdmin]
        else:
            self.permission_classes = [IsAuthenticated | ReadOnly]
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        build_version = request.headers.get("Build-Version")
        if not build_version:
            raise ValidationError("The 'Build-Version' header is required.")

        try:
            build_version = int(build_version)
        except ValueError:
            raise ValidationError("The 'Build-Version' header must be an integer.")

        data = request.data

        if build_version and int(build_version) < V2:
            # Old version: Accept a single menu ID
            menu_id = data.get("menu_id")
            vote_data = {
                "employee": request.user.employee.id,
                "menu": menu_id,
                "points": 1,
            }
        else:
            # New version: Accept up to 3 menu IDs with respective points
            votes = data.get("votes")
            for vote in votes:
                vote_data = {
                    "employee": request.user.employee.id,
                    "menu": vote["menu_id"],
                    "points": vote["points"],
                }
                serializer = self.get_serializer(data=vote_data)
                serializer.is_valid(raise_exception=True)
                self.perform_create(serializer)
            return Response(status=status.HTTP_201_CREATED)

        serializer = self.get_serializer(data=vote_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(
        detail=False,
        methods=["get"],
        url_path="results/today",
        permission_classes=[IsAuthenticated, IsAdmin],
    )
    def get_today_results(self, request):
        today = timezone.now().date()
        votes = Vote.objects.filter(menu__date=today)

        # Aggregate voting results
        results = {}
        for vote in votes:
            restaurant_name = vote.menu.restaurant.name
            if restaurant_name not in results:
                results[restaurant_name] = 0
            results[restaurant_name] += vote.points

        return Response(results)
