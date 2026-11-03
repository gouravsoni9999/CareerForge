from rest_framework.permissions import BasePermission
from .models import User


class IsStudent(BasePermission):
    message = "Only students can access this resource."

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == User.Role.STUDENT
        )

class IsRecruiter(BasePermission):
    message = "Only recruiters can access this resource."

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == User.Role.RECRUITER
        )

class IsAdmin(BasePermission):
    message = "Only administrators can access this resource."

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and (request.user.role == User.Role.ADMIN or request.user.is_superuser)
        )