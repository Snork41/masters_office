from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth import get_user_model

from .models import PostWalking, PostRepairWork, PostOrder, District, Personal

User = get_user_model()


def get_paginator(request, queryset, amount_posts):
    """Пагинация в журналах."""
    paginator = Paginator(queryset, amount_posts)
    page = request.GET.get('page')
    try:
        response = paginator.page(page)
    except PageNotAnInteger:
        response = paginator.page(1)
    except EmptyPage:
        response = paginator.page(paginator.num_pages)
    return response


def add_number_post(self, obj, model, username, commit, *args, **kwargs):
    """Сохранение записи в журнале с автоматической нумерацией.

    При создании записи обхода учитывается район.
    """
    if not obj.number_post:
        if model is PostWalking:
            most_recent = model.objects.filter(
                district=obj.district).order_by('-number_post').first()
        if model is PostRepairWork or model is PostOrder:
            most_recent = model.objects.all().order_by('-number_post').first()
        obj.number_post = most_recent.number_post + 1 if most_recent else 1
        if username:
            obj.author = username
    if commit:
        obj.save()
        self._save_m2m()
    return obj


def add_number_order(self, obj, model, *args, **kwargs):
    """Присвоение записи в журнале нарядов и распоряжений
    номера наряда/распоряжения."""
    if not obj.number_order:
        if obj.order == 'Наряд':
            most_recent = model.objects.filter(order='Наряд').order_by('-number_order').first()
        elif obj.order == 'Распоряжение':
            most_recent = model.objects.filter(order='Распоряжение').order_by('-number_order').first()
        obj.number_order = most_recent.number_order + 1 if most_recent else 1
    return obj


def filter_district(request):
    """Фильтрует выбор района в зависимости от энергорайона пользователя."""
    return District.objects.filter(energy_district=request.user.energy_district)


def filter_foreman(request):
    """Фильтрует выбор производителя работ в зависимости от энергорайона пользователя."""
    return Personal.objects.filter(energy_district=request.user.energy_district, foreman=True)


def filter_author(request):
    """Фильтрует выбор автора записи в зависимости от энергорайона пользователя."""
    return User.objects.filter(energy_district=request.user.energy_district)
