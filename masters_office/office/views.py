import logging

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import (
    ListView, TemplateView, DetailView, FormView, CreateView, UpdateView)


from .models import District, Journal, PostWalking, Resolution
from .forms import PostWalkingForm, ResolutionForm
from .utils import get_page


logger = logging.getLogger(__name__)


class HomePageView(TemplateView):
    template_name = 'office/index.html'


class CabinetView(LoginRequiredMixin, TemplateView):
    template_name = 'office/cabinet.html'


class JournalsListView(LoginRequiredMixin, ListView):
    model = Journal
    template_name = 'office/journals.html'
    context_object_name = 'all_journals'


class DistrictsListView(LoginRequiredMixin, ListView):
    model = District
    template_name = 'office/districts.html'
    context_object_name = 'districts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['journal'] = get_object_or_404(
            Journal, slug=self.kwargs.get('slug_journal')
        )
        return context


class JournalWalkView(LoginRequiredMixin, ListView):
    model = Journal
    template_name = 'office/journal_walk.html'
    context_object_name = 'journal'

    def get_queryset(self):
        return get_object_or_404(Journal, slug=self.kwargs.get('slug_journal'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['district'] = get_object_or_404(
            District, slug=self.kwargs.get('slug_district')
        )
        page_obj = get_page(self.request, context['journal'].posts.filter(
            district_id=context['district'].id).prefetch_related(
                'author', 'members')
        )
        context['page_obj'] = page_obj
        return context


@login_required
def create_post_walking(request, username, slug_journal, slug_district):
    district = get_object_or_404(District, slug=slug_district)
    journal = get_object_or_404(Journal, slug=slug_journal)
    initial_data = {'district': district, }
    form = PostWalkingForm(
        request.POST or None,
        files=request.FILES or None,
        initial=initial_data,
    )
    context = {
        'form': form,
    }
    if form.is_valid():
        post = form.save(False)
        post.author = request.user
        post.journal = journal
        form.save()
        logger.info(
            f'PostWalking (id: {post.id}) was created. '
            f'User: {(post.author.username).upper()}'
        )
        return redirect(
            'office:journal_walk',
            username, slug_journal, slug_district
        )
    return render(request, 'office/create_post_walking.html', context)


@login_required
def edit_post_walking(request, username, slug_journal, slug_district, post_id):
    post = get_object_or_404(PostWalking, id=post_id)
    if post.author != request.user:
        return redirect(
            'office:post_walking_detail',
            username, slug_journal, slug_district, post_id
        )
    form = PostWalkingForm(
        request.POST or None,
        files=request.FILES or None,
        instance=post,
    )
    fields_hidden = form.fields['district']
    fields_hidden.widget = fields_hidden.hidden_widget()
    context = {
        'post': post,
        'form': form,
        'is_edit': True
    }
    if request.method == 'POST':
        if form.is_valid():
            form.save(request.user)
            logger.info(
                f'PostWalking (id: {post.id}) was edited. '
                f'User: {(request.user.username).upper()}'
            )
            return redirect(
                'office:post_walking_detail',
                username, slug_journal, slug_district, post_id
            )
    return render(request, 'office/create_post_walking.html', context)


class PostWalkingDetailView(LoginRequiredMixin, DetailView, FormView):
    model = PostWalking
    template_name = 'office/post_walking_detail.html'
    pk_url_kwarg = 'post_id'
    context_object_name = 'post'
    form_class = ResolutionForm

    def get_queryset(self):
        return super().get_queryset().select_related(
            'author', 'journal', 'district')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['district'] = context['post'].district
        context['journal'] = context['post'].journal
        context['resolution'] = context['post'].resolution.first()
        return context


class ResolutionAddView(LoginRequiredMixin, CreateView):
    model = Resolution
    fields = ['text']

    def form_valid(self, form):
        if self.request.user.is_staff:
            resolution = form.save(commit=False)
            resolution.author = self.request.user
            resolution.post_walking_id = self.kwargs.get('post_id')
            resolution.save()
            messages.success(self.request, 'Резолюция успешно добавлена')
            logger.info(
                f'Resolution (id: {resolution.id}) was added. '
                f'Text: {resolution.text}. '
                f'User: {(resolution.author.username).upper()}'
            )
            return super().form_valid(form)
        return self.form_invalid(form=form, message=True)

    def form_invalid(self, form, message=False):
        if message:
            messages.warning(
                self.request, 'Резолюцию может оставлять только Начальник'
            )
        else:
            messages.warning(self.request, 'Резолюция не может быть пустой')
        return redirect('office:post_walking_detail',
                        self.kwargs.get('username'),
                        self.kwargs.get('slug_journal'),
                        self.kwargs.get('slug_district'),
                        self.kwargs.get('post_id')
                        )


class ResolutionEditView(LoginRequiredMixin, UpdateView):
    model = Resolution
    fields = ['text']
    template_name_suffix = '_update_form'

    def form_valid(self, form):
        messages.success(self.request, 'Резолюция изменена')
        logger.info(
            f'Resolution (id: {self.object.id}) was changed. '
            f'New text: {self.object.text}. '
            f'User: {(self.request.user.username).upper()}'
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, 'Резолюция не может быть пустой')
        return redirect(self.object.get_absolute_url())
