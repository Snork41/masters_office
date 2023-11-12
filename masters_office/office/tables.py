import django_tables2 as tables
import itertools

from django.utils.safestring import mark_safe

from .models import Personal, PostOrder
from masters_office.settings import EMPLOYEES_TABLE_TEMPLATE, POSTS_ORDER_TABLE_TEMPLATE


class PersonalTable(tables.Table):
    number_row = tables.Column(
        empty_values=(), orderable=False, verbose_name='№')

    def render_number_row(self):
        """Счетает и отображает номер строки таблицы"""
        self.number_row = getattr(
            self, 'number_row', itertools.count(self.page.start_index())
        )
        return next(self.number_row)

    class Meta:
        model = Personal
        template_name = EMPLOYEES_TABLE_TEMPLATE
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
    number_post = tables.Column(verbose_name='№', attrs={'td': {'class': 'text-center', 'style': 'width: 10%'}})
    district = tables.Column(attrs={'td': {'class': 'text-center', 'style': 'width: 10%'}})
    order = tables.Column(verbose_name='Оформление работ', attrs={'td': {'class': 'text-center', 'style': 'width: 10%'}})
    number_order = tables.Column(attrs={'td': {'class': 'text-center', 'style': 'width: 10%'}})
    description = tables.Column(attrs={'td': {'style': 'width: 100%'}})
    date_start_working = tables.Column(verbose_name='Работа начата', attrs={'td': {'style': 'width: 10%'}})
    is_deleted = tables.Column(attrs={'td': {'class': 'text-center', 'style': 'width: 10%'}})

    class Meta:
        model = PostOrder
        template_name = POSTS_ORDER_TABLE_TEMPLATE
        fields = (
            'number_post',
            'district',
            'order',
            'number_order',
            'description',
            'foreman',
            'date_start_working',
            'date_end_working',
            'is_deleted'
        )

    def render_is_deleted(self, value):
        if value:
            return mark_safe('<span style="color: red;">Да</span>')
        return 'Нет'

    def render_date_start_working(self, value):
        return value.strftime('%d.%m.%Y %H:%M')

    def render_date_end_working(self, value):
        if not value:
            return 'В работе'
        return mark_safe(f'<span style="color: rgb(0, 240, 70);">{value.strftime("%d.%m.%Y %H:%M")}</span>')
