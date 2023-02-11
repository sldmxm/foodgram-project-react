from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator

from django.conf import settings
from users.validators import validate_username_in_reserved_list


class User(AbstractUser):
    username = models.CharField(
        max_length=settings.STANDARD_MAX_CHAR_FIELD_LENGTH,
        unique=True,
        verbose_name='User name',
        validators=[
            validate_username_in_reserved_list,
            UnicodeUsernameValidator,
        ],
    )
    email = models.EmailField(
        unique=True,
        max_length=settings.EMAIL_MAX_CHAR_FIELD_LENGTH,
        verbose_name='Email address',
    )
    first_name = models.CharField(
        max_length=settings.STANDARD_MAX_CHAR_FIELD_LENGTH,
        verbose_name='First name',
    )
    last_name = models.CharField(
        max_length=settings.STANDARD_MAX_CHAR_FIELD_LENGTH,
        verbose_name='Last name',
    )

    REQUIRED_FIELDS = [
        'username',
        'first_name',
        'last_name',
    ]

    USERNAME_FIELD = 'email'

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
