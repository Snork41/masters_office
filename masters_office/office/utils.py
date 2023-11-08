from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from .models import PostWalking, PostRepairWork, PostOrder


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
