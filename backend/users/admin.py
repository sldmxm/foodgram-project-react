from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import UserCreationForm, UserChangeForm
from .models import User, Follow


class UserAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
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
    search_fields = ('username', 'first_name', 'last_name', 'email')
    filter = (

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


admin.site.register(User, UserAdmin)
