from rest_framework import permissions

class IsUser(permissions.BasePermission):
    """
    anyone can create a new user but only the user can view or change it's data
    """
    def has_object_permission(self, request, view, obj):
        if request.method =='POST':
            return True
        return obj == request.user    
class IsOwner(permissions.BasePermission):
    """
    Only the owner
    """
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user