# Generated by Django 4.2.14 on 2024-10-23 14:03

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('timeline', '0002_alter_post_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
