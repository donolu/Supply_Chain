from django.db import models
from django.contrib.auth.models import AbstractUser
from phone_field import PhoneField

# Create your models here.


class User(AbstractUser):
    is_customer = models.BooleanField(default=False)
    is_engineer = models.BooleanField(default=False)
    phone = PhoneField(blank=True, help_text="Contact phone number")
    profile_image = models.ImageField(upload_to="profile_pics", blank=True)

    class Meta:
        swappable = "AUTH_USER_MODEL"

    def __str__(self):
        return self.username
