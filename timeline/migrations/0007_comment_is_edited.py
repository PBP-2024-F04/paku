# Generated by Django 4.2.14 on 2024-10-27 03:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timeline', '0006_post_is_edited'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='is_edited',
            field=models.BooleanField(default=False),
        ),
    ]