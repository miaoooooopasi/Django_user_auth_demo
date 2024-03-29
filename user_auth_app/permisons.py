from rest_framework import permissions, request

# from user_auth_app.models import User


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
     Assumes the model instance has an `owner` attribute.
     所有者操作view
     """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        #  so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        # Instance must have an attribute named `owner`.

        return User.usernmae == request.username
