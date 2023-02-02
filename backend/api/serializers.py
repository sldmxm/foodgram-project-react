from rest_framework import serializers

from djoser.serializers import UserSerializer

from recipes.models import Tag, Recipe, RecipeIngredients, IngredientWithUnit, Ingredient
from users.models import User, Follow


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


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = (
            'id',
            'name',
            'color',
            'slug',
        )


class RecipeIngredientsSerializer(serializers.ModelSerializer):
    ingredient = serializers.SlugRelatedField(
        slug_field='ingredient.name',
        # queryset=IngredientWithUnit.objects.all(),
        read_only=True,
    )
    # measurement_unit = serializers.SlugRelatedField(
    #     slug_field='unit__id',
    #     read_only=True,
    # )

    class Meta:
        model = RecipeIngredients
        fields = (
            'id',
            'ingredient',
            # 'measurement_unit',
            'amount',
        )


class RecipeSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    tags = TagSerializer(many=True)
    ingredients = RecipeIngredientsSerializer(many=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )

    def get_is_favorited(self, obj):
        return (
                self.context['request'].user.is_authenticated
                and
                self.context['request'].user.favorite_recipes.filter(
                    id=obj.id
                ).exists()
                )

    def get_is_in_shopping_cart(self, obj):
        try:
            return (
                self.context['request'].user.is_authenticated
                and
                self.context['request'].user.cart.filter(
                    recipes=obj
                ).exists()
                )
        except User.cart.RelatedObjectDoesNotExist:
            return False
