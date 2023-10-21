import django_tables2 as tables

from .models import Personal


class PersonalTable(tables.Table):
    class Meta:
        model = Personal
        fields = (
            'tab_number',
            'first_name',
            'last_name',
            'middle_name',
            'position',
            'rank',
        )
