import django_tables2 as tables
import itertools

from .models import Personal


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
        fields = (
            'number_row',
            'tab_number',
            'first_name',
            'last_name',
            'middle_name',
            'position',
            'rank',
        )
