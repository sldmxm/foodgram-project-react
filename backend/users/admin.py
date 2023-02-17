from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Follow


class UserAdmin(UserAdmin):
    model = User
    list_display = (
            'username',
            'email',
            'first_name',
            'last_name',
        )
    list_filter = (
        'username',
        'email',
    )
    search_fields = (
        'username',
        'first_name',
        'last_name',
        'email',
    )
    fields = (
        'username',
        'email',
        'first_name',
        'last_name',
    )


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'follower',
        'author'
    )
    search_fields = ('follower', 'author', )
    list_filter = ('author', 'follower', )
    list_editable = ('author', 'follower', )


admin.site.register(User, )
