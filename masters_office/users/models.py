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
    energy_district = models.ForeignKey(
        'office.EnergyDistrict',
        on_delete=models.PROTECT,
        verbose_name='Энергорайон'
    )
    middle_name = models.CharField(
        max_length=50,
        verbose_name='Отчество'
    )

    def get_full_name(self):
        return f'{self.last_name} {self.first_name} {self.middle_name}'
