from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import TweetViewSet, CommentViewSet

router = DefaultRouter()
router.register(r'tweets', TweetViewSet)
router.register(r'comments', CommentViewSet)

urlpatterns = router.urls
