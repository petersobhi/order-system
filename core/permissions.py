from rest_framework import permissions


class IsSeller(permissions.BasePermission):
    """
    Custom permission to only allow seller of a product to modify or delete it.
    """

    def has_permission(self, request, view):
        return request.user

    def has_object_permission(self, request, view, obj):
        return obj.seller == request.user


class IsBuyer(permissions.BasePermission):
    """
    Custom permission to only allow buyer of an order to modify or delete it.
    """

    def has_permission(self, request, view):
        return request.user

    def has_object_permission(self, request, view, obj):
        return obj.buyer == request.user
