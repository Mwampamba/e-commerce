# Generated by Django 4.1.5 on 2023-01-30 04:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product_store', '0005_alter_rating_status'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='rating',
            options={'verbose_name': 'rating', 'verbose_name_plural': 'Product Rates'},
        ),
        migrations.AlterModelTable(
            name='rating',
            table='product_rate',
        ),
    ]
