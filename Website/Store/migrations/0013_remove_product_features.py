# Generated by Django 5.1 on 2024-08-10 09:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0012_alter_product_features'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='features',
        ),
    ]
