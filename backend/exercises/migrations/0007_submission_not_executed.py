# Generated by Django 3.0.5 on 2020-04-16 19:43

from django.db import (
    migrations,
    models,
)


class Migration(migrations.Migration):

    dependencies = [
        ('exercises', '0006_auto_20200416_1808'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='not_executed',
            field=models.BooleanField(default=False),
        ),
    ]
