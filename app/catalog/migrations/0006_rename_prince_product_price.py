# Generated by Django 4.2.4 on 2023-10-04 23:14

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("catalog", "0005_alter_product_sku"),
    ]

    operations = [
        migrations.RenameField(
            model_name="product",
            old_name="prince",
            new_name="price",
        ),
    ]