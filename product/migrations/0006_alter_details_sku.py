# Generated by Django 4.2.2 on 2023-07-24 16:09

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("product", "0005_alter_category_created_by"),
    ]

    operations = [
        migrations.AlterField(
            model_name="details",
            name="sku",
            field=models.CharField(blank=True, max_length=10, unique=True),
        ),
    ]