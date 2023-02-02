from django.contrib import admin

from cart.models import Cart
from .models import Recipe, Ingredient, IngredientUnit, RecipeIngredients, Tag


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
    list_filter = ('author', 'name', 'tags', )
    empty_value_display = 'n/a'
    list_editable = ('author', )
    exclude = ('favorite', )
    readonly_fields = ('favorite_count',)
    fields = (
        ('name',
         'favorite_count',
         ),
        'author',
        'text',
        'image',
        'tags',
        'cooking_time',
    )


class IngredientUnitInline(admin.TabularInline):
    model = Ingredient.unit.through
    extra = 1


@admin.register(IngredientUnit)
class IngredientUnitAdmin(admin.ModelAdmin):
    inlines = [
        IngredientUnitInline,
    ]


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    inlines = [
        IngredientUnitInline,
    ]
    exclude = ('unit', )
    list_display = (
        'name',
        'units',
    )
    search_fields = ('name', )
    list_filter = ('name', 'unit', )
    empty_value_display = 'n/a'

    def units(self, obj):
        return ", ".join([i.name for i in obj.unit.all()])


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
