from django.db import models

from users.models import User
from recipes.models import Recipe


class Cart(models.Model):
    user = models.OneToOneField(
        User,
        verbose_name='Cart owner',
        on_delete=models.CASCADE,
        related_name='cart',
    )
    recipes = models.ManyToManyField(
        Recipe,
        verbose_name='Recipes in cart',
    )

    def recipes_in_cart_count(self):
        return self.recipes.count()
