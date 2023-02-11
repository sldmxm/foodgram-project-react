from django.core.exceptions import ValidationError

from django.conf import settings


def validate_username_in_reserved_list(value):
    if value.lower() in settings.RESERVED_USERNAMES:
        raise ValidationError('This username is reserved.')
