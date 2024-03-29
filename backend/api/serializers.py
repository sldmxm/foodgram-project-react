from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from drf_extra_fields.fields import Base64ImageField

from recipes.models import (
    Tag,
    Recipe,
    RecipeIngredients,
    Ingredient,
)
from users.models import User, Follow
from api.validators import DoubleValidator


class UserSerializer(serializers.ModelSerializer):
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


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = (
            'id',
            'name',
            'measurement_unit',
        )


class RecipeIngredientsSerializer(serializers.ModelSerializer):
    name = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Ingredient.objects.all(),
        source='ingredient',
    )
    id = serializers.IntegerField(
        source='ingredient.id'
    )
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = RecipeIngredients
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount',
        )


class RecipeViewSerializer(serializers.ModelSerializer):
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
                self.context['request'].user.cart.recipes.filter(
                    id=obj.id
                ).exists()
                )
        except User.cart.RelatedObjectDoesNotExist:
            return False


class RecipeEditIngredientsSerializer(RecipeIngredientsSerializer):
    class Meta:
        model = RecipeIngredients
        fields = (
            'id',
            'amount',
        )


class RecipeEditSerializer(RecipeViewSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )
    tags = serializers.SlugRelatedField(
        slug_field='id',
        queryset=Tag.objects.all(),
        many=True,
    )
    image = Base64ImageField(
        allow_null=False,
        allow_empty_file=False,
    )
    ingredients = RecipeEditIngredientsSerializer(
        many=True,
    )

    class Meta:
        model = Recipe
        fields = (
            'tags',
            'author',
            'ingredients',
            'name',
            'image',
            'text',
            'cooking_time',
        )

    # нет идей, почему не работает
    # allow_null=False, allow_empty_file=False
    def validate_image(self, value):
        if not value:
            raise serializers.ValidationError('This field may not be blank.')
        return value

    def validate_cooking_time(self, value):
        if value < 1:
            raise serializers.ValidationError('One minute or more')
        return value

    def ingredients_and_tags_add(self, recipe, ingredients, tags):
        ingredients_update = []
        for ingredient in ingredients:
            ingredients_update.append(
                RecipeIngredients(
                    ingredient=Ingredient.objects.get(
                        id=ingredient['ingredient']['id']
                    ),
                    amount=ingredient['amount'],
                    recipe=Recipe.objects.get(id=recipe.id),
                )
            )
        RecipeIngredients.objects.bulk_create(
            ingredients_update,
            ignore_conflicts=True,
        )

        for tag in tags:
            recipe.tags.add(tag)

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        self.ingredients_and_tags_add(
            recipe=recipe,
            ingredients=ingredients,
            tags=tags
        )
        recipe.save()
        return recipe

    def update(self, instance, validated_data):

        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')

        RecipeIngredients.objects.filter(
            recipe_id=instance.id
        ).delete()

        for tag in instance.tags.all():
            instance.tags.remove(tag)

        self.ingredients_and_tags_add(
            recipe=instance,
            ingredients=ingredients,
            tags=tags
        )

        for field, value in validated_data.items():
            setattr(instance, field, value)

        instance.save()
        return instance


class ShortRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time',
        )


class SubscriptionsViewSerializer(UserSerializer):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
        )

    def get_recipes_count(self, obj):
        return obj.recipes.count()

    def get_recipes(self, obj):
        try:
            recipes_limit = int(
                self.context['request'].query_params.get('recipes_limit')
            )
            recipes = obj.recipes.all()[:recipes_limit]
        except Exception:
            recipes = obj.recipes.all()

        return ShortRecipeSerializer(recipes, many=True).data


class SubscriptionSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='id',
        default=serializers.CurrentUserDefault(),
    )
    follower = serializers.SlugRelatedField(
        read_only=True,
        slug_field='id',
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = Follow
        fields = (
            'follower',
            'author',
        )
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=fields,
            ),
            DoubleValidator(
                fields=fields,
                message="You can't follow yourself",
            ),
        ]
