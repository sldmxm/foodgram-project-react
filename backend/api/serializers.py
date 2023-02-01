from rest_framework import serializers

from djoser.serializers import UserSerializer

from recipes.models import Tag
from users.models import User, Follow


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('name', 'slug', 'color')


class UserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        )

    def get_is_subscribed(self, obj):
        return (
                self.context['request'].user.is_authenticated
                and
                Follow.objects.filter(
                    follower=self.context['request'].user,
                    author=obj
                ).exists()
                )

