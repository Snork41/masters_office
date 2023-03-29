from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    position = models.ForeignKey(
        'office.Position',
        related_name='master',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name='Должность'
    )
