from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """ Allow users to access their own records only. """

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True  # Admin can do anything
        if request.method in permissions.SAFE_METHODS:
            return True

        if hasattr(obj, 'student'):
            return obj.student.user == request.user
        elif hasattr(obj, 'enrollment'):
            return obj.enrollment.student.user == request.user
        elif hasattr(obj, 'payment'):
            return obj.payment.enrollment.student.user == request.user
        return False