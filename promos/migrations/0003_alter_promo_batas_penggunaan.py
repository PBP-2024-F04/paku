# Generated by Django 5.1.2 on 2024-10-25 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('promos', '0002_remove_promo_price_after_remove_promo_price_before_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='promo',
            name='batas_penggunaan',
            field=models.DateField(blank=True, null=True),
        ),
    ]
