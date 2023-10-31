from django import template

register = template.Library()


@register.filter
def is_digit(value):
    """Фильтр для выравнивания по центру столбца Разряд (таблица Сотрудников)"""
    return str(value).isdigit() or value == '—'
