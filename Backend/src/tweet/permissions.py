from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Permiso personalizado para permitir que solo el propietario de un tweet lo edite o elimine.
    """
    def has_object_permission(self, request, view, obj):
        # Los métodos de solo lectura (GET, HEAD, OPTIONS) están permitidos para cualquier usuario
        if request.method in permissions.SAFE_METHODS:
            return True

        # Solo el propietario del tweet puede editar o eliminar
        return obj.user == request.user
