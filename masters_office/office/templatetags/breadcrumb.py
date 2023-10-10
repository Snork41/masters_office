from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def get_breadcrumb(context):
    path = [x for x in context.request.path.split('/') if x]
    context['path'] = path[:-1]
    if context.request.resolver_match:
        context['kwargs'] = context.request.resolver_match.kwargs
    return context
