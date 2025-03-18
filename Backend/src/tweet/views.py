from rest_framework import viewsets, status, filters, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from .models import Tweet, Like, Comment, Notification
from .serializers import TweetSerializer, CommentSerializer
from .permissions import IsOwnerOrReadOnly

class TweetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class CommentPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class TweetViewSet(viewsets.ModelViewSet):
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer
    permission_classes = [IsAuthenticated,permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['content', 'user__username']
    pagination_class = TweetPagination

    def list(self, request, *args, **kwargs):
        # Asegúrate de que no haya tweets nulos en la respuesta
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  # Asigna el usuario autenticado al tweet

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        tweet = self.get_object()
        user = request.user
        like, created = Like.objects.get_or_create(user=user, tweet=tweet)
        if not created:
            return Response({'detail': 'Ya diste like a este tweet.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'detail': 'Like agregado.'}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['delete'])
    def unlike(self, request, pk=None):
        tweet = self.get_object()
        user = request.user
        like = Like.objects.filter(user=user, tweet=tweet).first()
        if like:
            like.delete()
            if tweet.likes_count > 0:  # Evita que likes_count sea negativo
                tweet.likes_count -= 1
                tweet.save()
            return Response({'detail': 'Like eliminado.'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'detail': 'No diste like a este tweet.'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def comments(self, request, pk=None):
        tweet = self.get_object()
        comments = Comment.objects.filter(tweet=tweet)
        serializer = CommentSerializer(comments, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='user/(?P<username>[^/.]+)')
    def user_tweets(self, request, username=None):
        tweets = Tweet.objects.filter(user__username=username).order_by('-created_at')
        paginator = TweetPagination()
        paginated_tweets = paginator.paginate_queryset(tweets, request)
        serializer = self.get_serializer(paginated_tweets, many=True)
        return paginator.get_paginated_response(serializer.data)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        # Asigna el usuario autenticado al comentario al crearlo
        tweet_id = self.request.data.get('tweet')  # Obtén el ID del tweet desde la solicitud
        serializer.save(user=self.request.user, tweet_id=tweet_id)

    def get_serializer_context(self):
        # Pasa el request al contexto del serializador
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
