from django.conf import settings
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

from django_ckeditor_5.fields import CKEditor5Field
from simple_history.models import HistoricalRecords

User = get_user_model()


class StaticBlock(models.Model):
    title = models.CharField('Название', max_length=32)
    content = CKEditor5Field(verbose_name='Контент', config_name='extends')

    class Meta:
        verbose_name = 'блок контента'
        verbose_name_plural = 'Блоки контента'

    def __str__(self):
        return self.title


class EnergyDistrict(models.Model):
    """Подразделение."""

    title = models.CharField(
        verbose_name='Энергорайон',
        max_length=35,
        unique=True
    )

    history = HistoricalRecords()

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
    energy_district = models.ForeignKey(
        'EnergyDistrict',
        on_delete=models.PROTECT,
        verbose_name='Энергорайон'
    )

    history = HistoricalRecords()

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

    history = HistoricalRecords()

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
        choices=settings.RANK,
        null=True,
        blank=True,
        verbose_name='Разряд'
    )
    tab_number = models.IntegerField(
        null=False,
        blank=False,
        unique=True,
        verbose_name='Табельный номер'
    )
    foreman = models.BooleanField(
        verbose_name='Может быть производителем работ',
        default=False
    )

    history = HistoricalRecords()

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

    history = HistoricalRecords()

    class Meta:
        verbose_name = 'Бригада'
        verbose_name_plural = 'Бригады'

    def __str__(self):
        return f'Бригада № {self.number}. Мастера {self.master}'


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
        blank=False
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
    is_deleted = models.BooleanField(
        default=False,
        verbose_name='Удаленная запись'
    )
    is_edit = models.BooleanField(
        default=False,
        verbose_name='Редактировано'
    )

    history = HistoricalRecords()

    class Meta:
        verbose_name = 'Запись в журнале обхода'
        verbose_name_plural = 'Записи в журналах обходов'
        ordering = ['-number_post']

    def get_next_post(self):
        return self.__class__.objects.get(
            district=self.district, number_post=self.number_post + 1)

    def get_previous_post(self):
        return self.__class__.objects.get(
            district=self.district, number_post=self.number_post - 1)

    def get_absolute_url(self):
        return reverse('office:post_walking_detail', kwargs={
            'slug_district': self.district.slug,
            'post_id': self.id
            }
        )

    def __str__(self):
        return f'Запись в журнале обходов теловых сетей № {self.number_post}'


class Resolution(models.Model):
    """Резолюция начальника района."""

    post_walking = models.ForeignKey(
        'PostWalking',
        verbose_name='Резолюция для записи',
        on_delete=models.SET_NULL,
        related_name='resolution',
        blank=True,
        null=True
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='resolution'
    )
    text = models.TextField(
        verbose_name='Текст резолюции'
    )
    created = models.DateTimeField(
        verbose_name='Дата создания резолюции',
        auto_now_add=True
    )
    viewed = models.BooleanField(
        verbose_name='Резолюция просмотрена',
        default=False
    )

    history = HistoricalRecords()

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
            'slug_district': self.post_walking.district.slug,
            'post_id': self.post_walking.id
            }
        )


class PostRepairWork(models.Model):
    """Запись в журнале ремонтных работ."""

    time_create = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    time_update = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата редактирования'
    )
    number_post = models.PositiveIntegerField(
        verbose_name='Номер записи',
        unique=True
    )
    district = models.ForeignKey(
        'District',
        blank=False,
        null=True,
        on_delete=models.SET_NULL,
        related_name='posts_repair',
        verbose_name='источник (район)'
    )
    order = models.CharField(
        choices=settings.ORDER,
        verbose_name='Работы по',
        help_text='наряду или распоряжению',
        null=False,
        blank=False,
        max_length=30
    )
    number_order = models.PositiveIntegerField(
        verbose_name='Номер распоряжения/наряда'
    )
    adress = models.CharField(
        verbose_name='Адрес (объект)',
        null=False,
        blank=False,
        max_length=200
    )
    description = models.TextField(
        verbose_name='Выполненные работы'
    )
    date_start_working = models.DateTimeField(
        verbose_name='Дата начала работ'
    )
    date_end_working = models.DateTimeField(
        verbose_name='Дата окончания работ'
    )
    author = models.ForeignKey(
        User,
        blank=False,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='Автор',
        related_name='posts_repair'
    )
    is_deleted = models.BooleanField(
        default=False,
        verbose_name='Удаленная запись'
    )
    is_edit = models.BooleanField(
        default=False,
        verbose_name='Редактировано'
    )

    history = HistoricalRecords()

    class Meta:
        verbose_name = 'Запись в журнале ремонтных работ'
        verbose_name_plural = 'Записи в журнале ремонтных работ'
        ordering = ['-number_post']

    def __str__(self):
        return f'Запись в журнале ремонтных работ № {self.number_post} от {self.time_create.date()}'

    @admin.display(description='Выполненные работы')
    def text_for_display(self):
        if len(self.description) > 15:
            return f'{self.description[:20]}...'
        return self.description

    def get_absolute_url(self):
        return reverse('office:journal_repair_work')


class PostOrder(models.Model):
    """Запись в журнале учета работ по нарядам и распоряжениям."""

    time_create = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    time_update = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата редактирования'
    )
    number_post = models.PositiveIntegerField(
        verbose_name='Номер записи',
        unique=True
    )
    district = models.ForeignKey(
        'District',
        blank=False,
        null=True,
        on_delete=models.SET_NULL,
        related_name='posts_order',
        verbose_name='источник (район)'
    )
    order = models.CharField(
        choices=settings.ORDER,
        verbose_name='Наряд/распоряжение',
        help_text='Номер присваивается автоматически',
        null=False,
        blank=False,
        max_length=30
    )
    number_order = models.PositiveIntegerField(
        verbose_name='Номер наряда/распоряжения'
    )
    description = models.TextField(
        verbose_name='Наименование работ'
    )
    foreman = models.ForeignKey(
        'Personal',
        blank=False,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='Производитель работ',
        related_name='post_order'
    )
    members = models.ManyToManyField(
        'Personal',
        related_name='post_order_brigade',
        verbose_name='Члены бригады',
        blank=False
    )
    date_start_working = models.DateTimeField(
        verbose_name='К работе приступили'
    )
    date_end_working = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='Работа закончена'
    )
    author = models.ForeignKey(
        User,
        blank=False,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='Автор',
        related_name='posts_order'
    )
    is_deleted = models.BooleanField(
        default=False,
        verbose_name='Удаленная запись'
    )

    history = HistoricalRecords()

    class Meta:
        verbose_name = 'Запись в журнале учета работ по нарядам и распоряжениям'
        verbose_name_plural = 'Записи в журнале учета работ по нарядам и распоряжениям'
        ordering = ['-number_post']

    def __str__(self):
        return f'Запись в журнале учета работ по нарядам и распоряжениям № {self.number_post}. {self.order} № {self.number_order}'
