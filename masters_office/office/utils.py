from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


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
