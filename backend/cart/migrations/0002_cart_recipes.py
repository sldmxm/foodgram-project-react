# Generated by Django 2.2.16 on 2023-01-25 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('recipes', '0001_initial'),
        ('cart', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='recipes',
            field=models.ManyToManyField(to='recipes.Recipe', verbose_name='Recipes in cart'),
        ),
    ]
