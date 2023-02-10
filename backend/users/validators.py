from django.core.exceptions import ValidationError

from backend import settings


def validate_username_in_reserved_list(value):
    if value in settings.RESERVED_USERNAMES:
        raise ValidationError('This username is reserved.')