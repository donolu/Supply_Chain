# Generated by Django 4.2.2 on 2023-07-13 12:10

from django.db import migrations, models
import phone_field.models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="user",
            options={},
        ),
        migrations.AddField(
            model_name="user",
            name="phone",
            field=phone_field.models.PhoneField(
                blank=True, help_text="Contact phone number", max_length=31
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="profile_image",
            field=models.ImageField(blank=True, upload_to="profile_pics"),
        ),
    ]
