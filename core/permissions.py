from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdmin(BasePermission):
    """Permission class to allow only admins."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_staff


class IsRestaurant(BasePermission):
    """Permission class to allow only restaurant users to create/update menus."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and hasattr(request.user, "restaurant")


class IsEmployee(BasePermission):
    """Permission class to allow only employees to vote."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and hasattr(request.user, "employee")


class ReadOnly(BasePermission):
    """Permission class to allow read-only access."""

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class IsVoteOwner(BasePermission):
    """Permission to allow only the owner of a vote to modify it."""

    def has_object_permission(self, request, view, obj):
        # Only the employee who created the vote can modify it
        return obj.employee.user == request.user


class IsRestaurantOwner(BasePermission):
    """
    Custom permission to allow only the owner of the restaurant to create, modify, or delete menus.
    """

    def has_permission(self, request, view):
        # Allow only authenticated users
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # `obj` here is a Menu instance, so we need to check its related restaurant's owner
        return obj.restaurant.owner == request.user
