from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def get_pagination_with_f(context, **kwargs):
    """Сохранение параметров фильтрации для пагинации."""
    path_parameters = context.request.GET.copy()
    for parameter, value in kwargs.items():
        if value:
            path_parameters[parameter] = value
    return path_parameters.urlencode()
