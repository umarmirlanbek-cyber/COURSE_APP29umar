from rest_framework.permissions import BasePermission

class StudentPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.role == 'student':
            return True
        return False

class TeacherPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'teacher'