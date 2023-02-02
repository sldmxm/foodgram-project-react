# Generated by Django 2.2.16 on 2023-02-01 08:36

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_auto_20230125_1332'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='color',
            field=models.CharField(max_length=16, unique=True, validators=[django.core.validators.RegexValidator(message='Color format error (#123456)', regex='^[\\w.@+-]+\\Z')], verbose_name='Tag color'),
        ),
    ]