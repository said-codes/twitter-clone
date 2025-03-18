from rest_framework import serializers
from .models import CustomUser, Notification
from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.ModelSerializer):
    followers = serializers.SerializerMethodField()
    following = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email','password', 'bio', 'profile_picture', 'followers', 'following']

    def get_followers(self, obj):
        return obj.followers.count()

    def get_following(self, obj):
        return obj.following.count()

    def create(self, validated_data):
        # Hashea la contraseña antes de guardar el usuario
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

    def get_profile_picture(self, obj):
        if obj.profile_picture:
            return self.context['request'].build_absolute_uri(obj.profile_picture.url)
        return None

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'

class ProfilePictureSerializer(serializers.ModelSerializer):
    profile_picture = serializers.ImageField(required=False)

    class Meta:
        model = CustomUser
        fields = ['profile_picture']

    def get_profile_picture(self, obj):
        if obj.profile_picture:
            return self.context['request'].build_absolute_uri(obj.profile_picture.url)
        return None
