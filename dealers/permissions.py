from rest_framework.permissions import BasePermission


class IsActiveStaff(BasePermission):
    """
    Allows access only to authenticated users who are marked as active staff members.
    """

    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and user.is_active and user.is_staff)



