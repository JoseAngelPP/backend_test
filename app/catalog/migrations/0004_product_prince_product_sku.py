# Generated by Django 4.2.4 on 2023-10-04 23:11

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("catalog", "0003_rename_brand_product_brand"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="prince",
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name="product",
            name="sku",
            field=models.CharField(default=""),
            preserve_default=False,
        ),
    ]