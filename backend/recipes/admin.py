from django.contrib import admin

from .models import (
    Recipe,
    Ingredient,
    RecipeIngredients,
    Tag,
    Cart,
)


class RecipeIngredientsInline(admin.TabularInline):
    model = RecipeIngredients
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = [
        RecipeIngredientsInline,
    ]
    list_display = (
        'name',
        'author',
        'favorite_count',
    )
    search_fields = ('name', )
    list_filter = (
        'author',
        'name',
        'tags',
    )
    empty_value_display = 'n/a'
    list_editable = ('author', )
    readonly_fields = ('favorite_count',)
    fields = (
        ('name',
         'favorite_count',
         ),
        'author',
        'text',
        'image',
        'cooking_time',
    )


class Ingredientmeasurement_unitInline(admin.TabularInline):
    model = Ingredient
    extra = 1


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'measurement_unit',
    )
    search_fields = ('name', )
    list_filter = ('name', 'measurement_unit', )
    empty_value_display = 'n/a'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    model = Tag
    list_display = (
        'name',
        'slug',
        'color',
    )
    search_fields = ('name', )
    list_filter = ('name', 'slug', )


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    model = Cart
    list_display = (
        'user',
        'recipes_in_cart_count'
    )
    search_fields = ('user', )
    list_filter = ('user', 'recipes')
