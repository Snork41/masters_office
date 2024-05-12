from django.db import models
from django.contrib.auth import get_user_model

from simple_history.models import HistoricalRecords

User = get_user_model()


class Notification(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        verbose_name='Пользователю',
        null=True
    )
    title = models.CharField(
        verbose_name='Заголовок',
        max_length=1024
    )
    content = models.TextField(
        verbose_name='Текст',
        null=True
    )
    viewed = models.BooleanField(
        verbose_name='Просмотрено?',
        default=False
    )
    time_create = models.DateTimeField(
        verbose_name='Дата создания',
        auto_now_add=True
    )
    link = models.CharField(
        verbose_name='Ссылка',
        max_length=1024,
        null=True,
        blank=True,
        help_text='Объект уведомления'
    )

    history = HistoricalRecords()

    class Meta:
        verbose_name = 'уведомление'
        verbose_name_plural = 'Уведомления'
        ordering = ('-time_create',)

    def __str__(self):
        return f'Уведомление (id {self.id}). Пользователю {self.user}'
