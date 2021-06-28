from django.db import models
from django.contrib.auth.models import AbstractUser


class UserRole(models.TextChoices):
    USER = 'user'
    ADMIN = 'admin'


class CustomUser(AbstractUser):
    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name='адрес электронной почты')
    role = models.CharField(
        max_length=30,
        choices=UserRole.choices,
        default=UserRole.USER,
    )

    class Meta:
        ordering = ['email']
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"

    def __str__(self):
        return self.first_name

    @property
    def is_admin(self):
        return (self.role == UserRole.ADMIN or self.is_staff
                or self.is_superuser)
