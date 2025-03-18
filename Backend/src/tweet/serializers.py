from rest_framework import serializers
from .models import Tweet, Like, Comment
from user.serializers import UserSerializer  # Importa el serializador de usuario


class TweetSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  # Incluye la información completa del usuario
    is_liked = serializers.SerializerMethodField()  # Campo calculado

    class Meta:
        model = Tweet
        fields = ['id', 'content', 'user', 'created_at','likes_count','is_liked']
        read_only_fields = ['user', 'created_at']  # El usuario y la fecha se asignan automáticamente

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Like.objects.filter(user=request.user, tweet=obj).exists()
        return False

    def get_user(self, obj):
        return {
            'username': obj.user.username,
            'profile_picture': self.context['request'].build_absolute_uri(obj.user.profile_picture.url),
        }
class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'user', 'tweet', 'created_at']
        read_only_fields = ['user', 'created_at']  # El usuario y la fecha se asignan automáticamente

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()  # Usamos un campo personalizado para el usuario

    class Meta:
        model = Comment
        fields = ['id', 'user', 'tweet', 'content', 'created_at']
        read_only_fields = ['user','tweet', 'created_at']  # Campos de solo lectura

    def get_user(self, obj):
        # Verifica si el usuario tiene una imagen de perfil
        if obj.user.profile_picture:
            profile_picture_url = self.context['request'].build_absolute_uri(obj.user.profile_picture.url)
        else:
            profile_picture_url = None

        return {
            'username': obj.user.username,
            'profile_picture': profile_picture_url,  # Devuelve la URL absoluta de la imagen
        }
    def get_serializer_context(self):
        # Pasa el request al contexto del serializador
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


