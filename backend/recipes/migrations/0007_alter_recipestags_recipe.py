# Generated by Django 4.1.6 on 2023-02-04 08:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0006_auto_20230204_0609'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipestags',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipe_tags', to='recipes.recipe'),
        ),
    ]
