from django.contrib import admin
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

from masters_office.settings import RANK


User = get_user_model()


class EnergyDistrict(models.Model):
    """Подразделение."""

    title = models.CharField(
        verbose_name='Энергорайон',
        max_length=20,
        unique=True
    )

    class Meta:
        verbose_name = 'Энергорайон'
        verbose_name_plural = 'Энергорайоны'

    def __str__(self):
        return self.title


class District(models.Model):
    """Источник тепла (котельная, ЦТП, ИТП)."""

    title = models.CharField(
        verbose_name='Источник тепла',
        max_length=100
    )
    slug = models.SlugField(
        null=False,
        unique=True
    )
    master = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='district',
        verbose_name='Ответственный'
    )

    class Meta:
        verbose_name = 'Источник тепла'
        verbose_name_plural = 'Источники тепла'

    def __str__(self):
        return self.title


class Position(models.Model):
    """Перечень должностей."""

    name_position = models.CharField(
        verbose_name='Должность',
        max_length=50
    )
    walker = models.BooleanField(
        verbose_name='Может участвовать в обходах'
    )

    class Meta:
        verbose_name = 'Должность'
        verbose_name_plural = 'Должности'
        ordering = ['name_position']

    def __str__(self):
        return self.name_position


class Personal(models.Model):
    """Сотрудник."""

    first_name = models.CharField(
        max_length=50,
        verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=50,
        verbose_name='Фамилия'
    )
    middle_name = models.CharField(
        max_length=50,
        verbose_name='Отчество'
    )
    energy_district = models.ForeignKey(
        'EnergyDistrict',
        on_delete=models.PROTECT,
        related_name='personal',
        verbose_name='Энергорайон'
    )
    position = models.ForeignKey(
        'Position',
        on_delete=models.PROTECT,
        related_name='personal',
        verbose_name='Должность'
    )
    rank = models.IntegerField(
        choices=RANK,
        null=True,
        blank=True,
        verbose_name='Разряд'
    )
    tab_number = models.SmallIntegerField(
        null=False,
        blank=False,
        unique=True,
        verbose_name='Табельный номер'
    )

    class Meta:
        verbose_name = 'Работник'
        verbose_name_plural = 'Работники'
        ordering = ['last_name']

    def __str__(self):
        return f'{self.last_name} {self.first_name} {self.middle_name}'


class Brigade(models.Model):
    """Бригада."""

    number = models.PositiveIntegerField(
        unique=True,
        verbose_name='Номер бригады'
    )
    master = models.ForeignKey(
        User, on_delete=models.PROTECT,
        verbose_name='Бригада мастера',
        null=True,
        blank=True
    )
    brigadier = models.ForeignKey(
        'Personal',
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        verbose_name='Бригадир',
        related_name='brigadier'
    )
    members = models.ManyToManyField(
        'Personal',
        related_name='brigades',
        verbose_name='Члены бригады'
    )

    class Meta:
        verbose_name = 'Бригада'
        verbose_name_plural = 'Бригады'

    def __str__(self):
        return f'Бригада № {self.number}. Мастера {self.master}'


class Journal(models.Model):
    """Журнал."""

    title = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Название'
    )
    slug = models.SlugField(
        null=False,
        unique=True
    )
    description = models.TextField(
        verbose_name='Описание'
    )

    class Meta:
        verbose_name = 'Журнал'
        verbose_name_plural = 'Журналы'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('office:districts', kwargs={
            'slug_journal': self.slug
            }
        )


class PostWalking(models.Model):
    """Запись в журнале обхода."""

    time_create = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    time_update = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата редактирования'
    )
    number_post = models.PositiveIntegerField(
        verbose_name='Номер записи'
    )
    walk_date = models.DateField(
        verbose_name='Дата обхода',
        help_text='Введите дату в формате "ДД.ММ.ГГГГ"'
    )
    planned = models.BooleanField(
        default=True,
        verbose_name='Плановый'
    )
    not_planned = models.BooleanField(
        default=False,
        verbose_name='Внеплановый'
    )
    district = models.ForeignKey(
        'District',
        blank=False,
        null=True,
        on_delete=models.SET_NULL,
        related_name='posts',
        verbose_name='источник'
    )
    members = models.ManyToManyField(
        'Personal',
        related_name='brigade',
        verbose_name='Члены бригады',
        blank=False,
    )
    task = models.TextField(
        max_length=250,
        verbose_name='Участок теплотрассы, задание мастера',
        default='Обход тепловой сети'
    )
    text = models.TextField(
        verbose_name='Замечания, выявленные при обходе'
    )
    plan = models.TextField(
        default='---',
        blank=True,
        verbose_name='Организационные мероприятия по устранению'
    )
    fix_date = models.DateField(
        null=True,
        blank=True,
        verbose_name='Дата устранения замечания',
        help_text='При отсутствии замечаний не заполняется'
    )
    transfer = models.CharField(
        max_length=150,
        default='---',
        blank=True,
        verbose_name='Перенос на ремонт в план на следующий месяц или на межотопительный период'
    )
    author = models.ForeignKey(
        User,
        blank=False,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='Автор',
        related_name='posts'
    )
    journal = models.ForeignKey(
        'Journal',
        null=True,
        on_delete=models.SET_NULL,
        related_name='posts',
        verbose_name='Журнал',
        help_text='Журнал, в котором будет запись'
    )
    is_deleted = models.BooleanField(
        default=False,
        verbose_name='Удаленная запись'
    )

    class Meta:
        verbose_name = 'Запись в журнале обхода'
        verbose_name_plural = 'Записи в Журналах обходов'
        ordering = ['-number_post']

    def get_next_post(self):
        return self.__class__.objects.get(
            district=self.district, number_post=self.number_post + 1)

    def get_previous_post(self):
        return self.__class__.objects.get(
            district=self.district, number_post=self.number_post - 1)

    def get_absolute_url(self):
        return reverse('office:post_walking_detail', kwargs={
            'slug_journal': self.journal.slug,
            'slug_district': self.district.slug,
            'post_id': self.id
            }
        )

    def __str__(self):
        return f'{self.district.title}, Запись № {self.number_post} от {self.time_create.date()}'

    @admin.display(description='Замечания, выявленные при обходе')
    def text_for_display(self):
        if len(self.text) > 15:
            return f'{self.text[:20]}...'
        return self.text


class Resolution(models.Model):
    """Резолюция начальника района."""

    post_walking = models.ForeignKey(
        'PostWalking',
        verbose_name='Резолюция для записи',
        on_delete=models.CASCADE,
        related_name='resolution',
        blank=True,
        null=True,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='resolution',
    )
    text = models.TextField(
        verbose_name='Резолюция начальника энергорайона',
    )
    created = models.DateTimeField(
        verbose_name='Дата создания резолюции',
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'Резолюция'
        verbose_name_plural = 'Резолюции'

    def __str__(self):
        return self.text

    def save(self, *args, **kwargs):
        if (Resolution.objects.filter(id=self.id) or
            not Resolution.objects.filter(
                post_walking_id=self.post_walking_id
        )):
            super(Resolution, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('office:post_walking_detail', kwargs={
            'slug_journal': self.post_walking.journal.slug,
            'slug_district': self.post_walking.district.slug,
            'post_id': self.post_walking.id
            }
        )
