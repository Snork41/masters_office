from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def get_breadcrumb(context):
    context['path'] = [x for x in context.request.path.split('/') if x]
    if context.request.resolver_match:
        context['kwargs'] = context.request.resolver_match.kwargs
    return context
