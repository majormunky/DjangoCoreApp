from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class Location(models.Model):
    name = models.CharField(max_length=64)


class UserPreferences(models.Model):
    location = models.ForeignKey(
        Location, blank=True, null=True, on_delete=models.SET_NULL
    )
    timezone = models.CharField(max_length=64, blank=True, null=True)


class CoreUserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Email is required")

        user_prefs = UserPreferences()
        user_prefs.save()

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.user_prefs = user_prefs
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True")

        return self._create_user(email, password, **extra_fields)


class CoreUser(AbstractUser):
    username = None
    email = models.EmailField("email address", unique=True)
    preferences = models.OneToOneField(
        UserPreferences, on_delete=models.CASCADE, blank=True, null=True
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CoreUserManager()

    def __str__(self):
        return self.email