from django.db import models

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
    # СДЕЛАТЬ ВАЛИДАТОР ДЛЯ ПОЛЯ ЦВЕТА
    color = models.CharField(
        'Tag color',
        max_length=16,
        null=False,
        unique=True,
    )

    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField(
        'Recipe name',
        max_length=250,
        blank=False,
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
    tag = models.ManyToManyField(
        Tag,
        related_name='recipes',
        blank=True,
    )
    cooking_time = models.IntegerField(
        'cooking time',
        null=True,
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


class IngredientUnit(models.Model):
    name = models.CharField(
        'Measurement unit',
        max_length=16,
        null=False,
        unique=True,
    )

    def __str__(self):
        return f'{self.name}'

    class Meta:
        ordering = ('name',)


class Ingredient(models.Model):
    name = models.CharField(
        'Ingredient name',
        max_length=150,
        db_index=True,
        unique=True,
    )
    unit = models.ManyToManyField(
        IngredientUnit,
        verbose_name='Ingredient measurement unit',
        related_name='ingredients',
        through='IngredientsUnits'
    )

    def __str__(self):
        return f'{self.name} ({self.unit})'

    class Meta:
        ordering = ('name',)


class IngredientsUnits(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        verbose_name='Ingredient',
        on_delete=models.CASCADE,
        null=False,
        related_name='ingredients_with_unit',
    )
    unit = models.ForeignKey(
        IngredientUnit,
        verbose_name='Ingredient measurement unit',
        on_delete=models.CASCADE,
        null=False,
        related_name='ingredients_with_unit',
    )

    def __str__(self):
        return f'{self.ingredient.name} ({self.unit.name})'

    class Meta:
        ordering = ('ingredient__name',)


class RecipeIngredients(models.Model):
        ingredient = models.ForeignKey(
            IngredientsUnits,
            verbose_name='Ingredient with measurement unit',
            on_delete=models.CASCADE,
            null=False,
        )
        recipe = models.ForeignKey(
            Recipe,
            verbose_name='Recipe',
            on_delete=models.CASCADE,
            null=False,
        )
        amount = models.IntegerField('amount of ingredient')
