from django.http import request
from rest_framework import permissions 


class IsToDoAuthor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        print('-----------------------------------------------------')
        print(request.user)
        return obj.user == request.user