# Generated by Django 3.0.5 on 2020-04-22 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exercises', '0014_auto_20200422_1012'),
    ]

    operations = [
        migrations.AlterField(
            model_name='errorcount',
            name='counter',
            field=models.PositiveIntegerField(default=0, verbose_name="compteur de l'erreur"),
        ),
    ]