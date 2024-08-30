from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)


class FullDjangoModelPermissions(permissions.DjangoModelPermissions):
    def __init__(self):
        self.perms_map['GET'] = ['%(app_label)s.view_%(model_name)s']


class ViewHistoryPermissions(permissions.DjangoModelPermissions):
    def has_permission(self, request, view):
        # Syntax: app_name.permission_name
        # If this returns true, then the user is gonna had permission and will be able to  access the history
        return request.user.has_perm('store.view_history')