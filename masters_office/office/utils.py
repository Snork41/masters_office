from django.core.paginator import Paginator

from masters_office.settings import AMOUNT_POSTS_WALK


def get_page(request, posts_walk_list):
    paginator = Paginator(posts_walk_list, AMOUNT_POSTS_WALK)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)
