from rest_framework import permissions

class IsMerchant(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
        logged_in_user = request.user
        return logged_in_user.role == "MERCHANT" and obj.merchant == logged_in_user
 