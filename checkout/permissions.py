from rest_framework import permissions
from rest_framework import exceptions

class IsMerchant(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
        logged_in_user = request.user
        if logged_in_user.role != "Merchant":
            raise exceptions.PermissionDenied({"Error": "You should be a merchant to access this endpoint"})
        
        return True
        