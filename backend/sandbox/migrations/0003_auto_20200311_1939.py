# Generated by Django 3.0.4 on 2020-03-11 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sandbox', '0002_sandboxprofile_image_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sandboxprofile',
            name='image_id',
            field=models.CharField(blank=True, max_length=60, null=True),
        ),
    ]
