# Generated by Django 2.2.16 on 2023-02-01 08:38

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20230201_0836'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=150, unique=True, validators=[django.core.validators.RegexValidator(message='Username format error (^[\\w.@+-]+\\z)', regex='^[\\w.@+-]+\\Z')], verbose_name='User name'),
        ),
    ]
