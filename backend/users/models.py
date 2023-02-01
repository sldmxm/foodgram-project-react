from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = models.CharField(
        max_length=150,
        unique=True,
        blank=False,
        verbose_name='User name',
    )
    email = models.EmailField(
        blank=False,
        unique=True,
        max_length=254,
        verbose_name='Email address',
    )
    first_name = models.CharField(
        max_length=150,
        blank=False,
        verbose_name='First name',
    )
    last_name = models.CharField(
        max_length=150,
        blank=False,
        verbose_name='Last name',
    )

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.is_superuser

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class Follow(models.Model):
    follower = models.ForeignKey(
        User,
        verbose_name='Follower',
        related_name='follow',
        on_delete=models.CASCADE,
    )
    author = models.ForeignKey(
        User,
        verbose_name='Author',
        related_name='followers',
        on_delete=models.CASCADE,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['follower', 'author'],
                name='unique_following',
            ),
            models.CheckConstraint(
                check=~models.Q(follower=models.F('author')),
                name='restrict_self_follow',
            ),
        ]
