# Generated by Django 5.1 on 2024-08-11 08:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0023_alter_product_booth'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='booth',
            field=models.ForeignKey(default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='Store.booth'),
        ),
    ]
