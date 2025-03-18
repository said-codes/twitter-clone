from rest_framework import viewsets
from .models import CustomUser
from .serializers import UserSerializer, NotificationSerializer, ProfilePictureSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated , AllowAny
from user.models import Notification
from rest_framework import filters


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'email']

    @action(detail=True, methods=['put'], url_path='update-profile-picture')
    def update_profile_picture(self, request, pk=None):
        user = self.get_object()
        serializer = ProfilePictureSerializer(user, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def follow(self, request, pk=None):
        user_to_follow = self.get_object()
        user = request.user
        if user == user_to_follow:
            return Response({'detail': 'No puedes seguirte a ti mismo.'}, status=status.HTTP_400_BAD_REQUEST)
        user.following.add(user_to_follow)

        # Crear notificación
        Notification.objects.create(
            user=user_to_follow,
            message=f"{user.username} comenzó a seguirte."
        )
        return Response({'detail': f'Ahora sigues a {user_to_follow.username}.'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def unfollow(self, request, pk=None):
        user_to_unfollow = self.get_object()
        user = request.user
        user.following.remove(user_to_unfollow)
        return Response({'detail': f'Dejaste de seguir a {user_to_unfollow.username}.'}, status=status.HTTP_200_OK)


class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)
