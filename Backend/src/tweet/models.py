from django.db import models
from user.models import CustomUser
from django.core.validators import MinValueValidator

class Tweet(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.CharField(max_length=280)
    created_at = models.DateTimeField(auto_now_add=True)
    likes_count = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])  # Evita valores negativos

    def __str__(self):
        return f"{self.user.username}: {self.content[:50]}"

class Like(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'tweet')  # Evita likes duplicados

    def __str__(self):
        return f"{self.user.username} likes {self.tweet.content[:50]}"

    def save(self, *args, **kwargs):
        # Incrementa el contador de likes al crear un like
        if not self.pk:  # Verifica si es un nuevo like
            self.tweet.likes_count += 1
            self.tweet.save()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.tweet.likes_count > 0:  # Evita que likes_count sea negativo
            self.tweet.likes_count -= 1
            self.tweet.save()
        super().delete(*args, **kwargs)

class Comment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, related_name='comments')
    content = models.CharField(max_length=280)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.content[:50]}"

class Notification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notificación para {self.user.username}: {self.message[:50]}"
