from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
User = get_user_model()


class Follow(models.Model):
    """Подписки"""
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='follower', verbose_name='Текущий пользователь')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='following', verbose_name='Понравившийся автор')