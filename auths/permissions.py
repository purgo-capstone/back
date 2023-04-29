from rest_framework.permissions import BasePermission

class isAdmin(BasePermission):
    '''
    IsAdmin permission - delete later if not used
    '''
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_admin