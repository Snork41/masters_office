from django.views.generic.base import TemplateView
from office.models import StaticBlock


class HelpView(TemplateView):
    template_name = 'about/help.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['about'] = StaticBlock.objects.filter(title='О сайте').first()
        return context

class ContactsView(TemplateView):
    template_name = 'about/contacts.html'
