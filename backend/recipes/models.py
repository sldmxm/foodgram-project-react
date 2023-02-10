from django.db import models
from django.core.validators import RegexValidator, MinValueValidator

from backend import settings
from users.models import User


class Tag(models.Model):
    name = models.CharField(
        'Recipe tag',
        max_length=32,
        null=False,
        unique=True,
    )
    slug = models.SlugField(
        'Recipe tag slug',
        max_length=16,
        null=False,
        unique=True,
    )
    color = models.CharField(
        'Tag color',
        max_length=16,
        null=False,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^#(?:[0-9a-fA-F]{3}){1,2}$',
                message='Color format error (#AABBCC or #ABC)',
            )
        ],
    )

    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField(
        'Recipe name',
        max_length=200,
        db_index=True,
    )
    text = models.TextField(
        'Recipe description',
        blank=True
    )
    author = models.ForeignKey(
        User,
        verbose_name='Recipe author',
        on_delete=models.CASCADE,
        null=False,
        related_name='recipes',
    )
    image = models.ImageField(
        'Recipe photo',
        upload_to='recipes_photos/',
        blank=True,
    )
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name='recipes',
    )
    cooking_time = models.IntegerField(
        'cooking time',
        null=True,
        validators=[MinValueValidator(
            limit_value=1,
            message='One minute or more'
        )]
    )
    favorite = models.ManyToManyField(
        User,
        related_name='favorite_recipes',
        blank=True,
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Publish date',
    )

    def __str__(self):
        return self.name

    def favorite_count(self):
        return self.favorite.count()

    class Meta:
        ordering = ('-pub_date',)


class Ingredient(models.Model):
    name = models.CharField(
        'Ingredient name',
        max_length=settings.STANDARD_MAX_CHAR_FIELD_LENGTH,
        db_index=True,
    )
    measurement_unit = models.CharField(
        'Measurement unit',
        max_length=16,
        null=False,
    )

    def __str__(self):
        return f'{self.name} ({self.measurement_unit})'

    class Meta:
        ordering = ('name',)


class RecipeIngredients(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        verbose_name='Ingredient with measurement unit',
        on_delete=models.CASCADE,
        null=False,
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Recipe',
        on_delete=models.CASCADE,
        null=False,
        related_name='ingredients',
    )
    amount = models.IntegerField('amount of ingredient')


class Cart(models.Model):
    user = models.OneToOneField(
        User,
        verbose_name='Cart owner',
        on_delete=models.CASCADE,
        related_name='cart',
    )
    recipes = models.ManyToManyField(
        Recipe,
        verbose_name='Recipef'
                     's in cart',
    )

    def recipes_in_cart_count(self):
        return self.recipes.count()

