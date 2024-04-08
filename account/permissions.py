from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwnerOrReadOnly(BasePermission):
    message = 'You must be the owner of this object.'

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.id == request.user.id
    
    def has_permission(self, request, view):
        if request.method == 'POST':
            return request.user.is_anonymous
        
        return True