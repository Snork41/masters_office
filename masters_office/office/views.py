import logging

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import (
    ListView, TemplateView, DetailView, FormView, CreateView, UpdateView)

from .models import Brigade, District, Journal, PostWalking, Personal, Resolution
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
                'author', 'members', 'district')
        )
        context['page_obj'] = page_obj
        return context


class PostWalkingCreateView(LoginRequiredMixin, CreateView):
    model = PostWalking
    template_name = 'office/create_post_walking.html'
    form_class = PostWalkingForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['journal'] = get_object_or_404(
            Journal, slug=self.kwargs.get('slug_journal')
        )
        return context

    def get_initial(self):
        initial = super().get_initial()
        initial['district'] = get_object_or_404(
            District, slug=self.kwargs.get('slug_district')
        )
        return initial

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        post.journal = get_object_or_404(
            Journal, slug=self.kwargs.get('slug_journal')
        )
        post.save()
        return super().form_valid(form)

    def get_success_url(self):
        logger.info(
            f'PostWalking (pk: {self.object.id}) was created. '
            f'User: {(self.object.author.username).upper()}'
        )
        messages.success(
            self.request,
            f'Запись № {self.object.number_post} успешно добавлена'
        )
        return reverse('office:journal_walk', kwargs={
                 'slug_journal': self.kwargs.get('slug_journal'),
                 'slug_district': self.kwargs.get('slug_district'),
            })


class PostWalkingEditView(LoginRequiredMixin, UpdateView):
    model = PostWalking
    template_name = 'office/edit_post_walking.html'
    form_class = PostWalkingForm
    pk_url_kwarg = 'post_id'
    context_object_name = 'post'

    def get_queryset(self):
        return super().get_queryset().select_related(
            'author', 'district')

    def dispatch(self, request, *args, **kwargs):
        post = self.get_object()
        if post.author != request.user:
            return redirect(
                'office:post_walking_detail',
                slug_journal=self.kwargs.get('slug_journal'),
                slug_district=self.kwargs.get('slug_district'),
                post_id=self.kwargs.get('post_id')
            )
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['journal'] = get_object_or_404(
            Journal, slug=self.kwargs.get('slug_journal')
        )
        return context

    def get_success_url(self):
        logger.info(
            f'PostWalking (pk: {self.object.id}) was edited. '
            f'User: {(self.object.author.username).upper()}'
        )
        messages.success(
            self.request,
            f'Запись № {self.object.number_post} успешно изменена'
        )
        return reverse('office:journal_walk', kwargs={
                 'slug_journal': self.kwargs.get('slug_journal'),
                 'slug_district': self.kwargs.get('slug_district'),
            })


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
    template_name = 'office/includes/resolution_form.html'
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
                        self.kwargs.get('slug_journal'),
                        self.kwargs.get('slug_district'),
                        self.kwargs.get('post_id')
                        )


class ResolutionEditView(LoginRequiredMixin, UpdateView):
    model = Resolution
    fields = ['text']
    template_name = 'office/includes/resolution_update_form.html'
    pk_url_kwarg = 'resolution_id'

    def form_valid(self, form):
        messages.success(self.request, 'Резолюция успешно изменена')
        logger.info(
            f'Resolution (id: {self.object.id}) was changed. '
            f'New text: {self.object.text}. '
            f'User: {(self.request.user.username).upper()}'
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, 'Резолюция не может быть пустой')
        return redirect(self.object.get_absolute_url())


class BrigadesListView(LoginRequiredMixin, ListView):
    model = Brigade
    template_name = 'office/brigades.html'
    context_object_name = 'brigades'

    def get_queryset(self):
        return Brigade.objects.filter(
            master__energy_district=self.request.user.energy_district
            ).prefetch_related('members__position', 'master', 'brigadier')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['energy_district'] = self.request.user.energy_district
        return context


class EmployeesListView(LoginRequiredMixin, ListView):
    model = Personal
    template_name = 'office/employees.html'
    context_object_name = 'employees'

    def get_queryset(self):
        return Personal.objects.filter(
            energy_district=self.request.user.energy_district
            ).select_related('position')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['energy_district'] = self.request.user.energy_district
        return context
