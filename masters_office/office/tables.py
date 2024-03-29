import django_tables2 as tables
import itertools
import pytz

from django.conf import settings
from django.utils.safestring import mark_safe
from django.urls import reverse

from .models import Personal, PostOrder


class PersonalTable(tables.Table):
    number_row = tables.Column(
        empty_values=(),
        orderable=False,
        verbose_name='№',
        attrs={'td': {'class': 'text-center'}}
    )
    tab_number = tables.Column(
        verbose_name='Таб. №',
        attrs={'td': {'class': 'text-center', 'style': 'width: 10%'}}
    )
    rank = tables.Column(
        attrs={'td': {'class': 'text-center', 'style': 'width: 10%'}}
    )

    def render_number_row(self):
        """Счетает и отображает номер строки таблицы"""
        self.number_row = getattr(
            self, 'number_row', itertools.count(self.page.start_index())
        )
        return next(self.number_row)

    class Meta:
        model = Personal
        template_name = settings.EMPLOYEES_TABLE_TEMPLATE
        fields = (
            'number_row',
            'tab_number',
            'first_name',
            'last_name',
            'middle_name',
            'position',
            'rank',
        )


class PostOrderTable(tables.Table):
    number_post = tables.Column(
        verbose_name='№',
        attrs={'td': {'class': 'text-center'}}
    )
    district = tables.Column()
    order = tables.Column(
        verbose_name='Оформление работ'
    )
    number_order = tables.Column(
        verbose_name='Номер'
    )
    description = tables.Column()
    date_start_working = tables.Column(
        verbose_name='Работа начата'
    )
    redact = tables.Column(
        verbose_name='Автор (изменить)',
        empty_values=(),
        orderable=False,
        attrs={'td': {'class': 'text-center'}}
    )
    is_deleted = tables.Column()

    class Meta:
        model = PostOrder
        template_name = settings.POSTS_ORDER_TABLE_TEMPLATE
        fields = (
            'number_post',
            'district',
            'order',
            'number_order',
            'description',
            'foreman',
            'date_start_working',
            'date_end_working',
            'redact',
            'is_deleted',
        )
        attrs = {
            'class': 'table table-bordered table-hover',
            'thead': {'class': 'table-light sticky-top sticky-offset-table'}
        }

    def render_redact(self, value, *args, **kwargs):
        url = reverse('office:edit_post_order', kwargs={'post_id': kwargs.get('record').id})
        if self.request.user == kwargs['record'].author:
            link = f'<a href="{url}" class="text-reset"><i class="bi bi-pencil-square"></i></a>'
            return mark_safe(link)
        return mark_safe(kwargs["record"].author)

    def render_is_deleted(self, value):
        if value:
            return mark_safe('<span style="color: red;">Да</span>')
        return 'Нет'

    def render_date_start_working(self, value):
        target_timezone = pytz.timezone(settings.TIME_ZONE)
        value = value.astimezone(target_timezone)
        return value.strftime('%d.%m.%Y %H:%M')

    def render_date_end_working(self, value):
        if not value:
            return 'В работе'
        target_timezone = pytz.timezone(settings.TIME_ZONE)
        value = value.astimezone(target_timezone)
        return mark_safe(f'<span style="color: rgb(0, 240, 70);">{value.strftime("%d.%m.%Y %H:%M")}</span>')
