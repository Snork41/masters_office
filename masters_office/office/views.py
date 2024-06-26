from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.views.generic import (CreateView, DetailView, FormView, ListView,
                                  TemplateView, UpdateView)
from django_filters.views import FilterView
from django_tables2 import SingleTableMixin

from core.services import create_notification,  view_notification, create_notification_view_resolution
from .filters import PersonalFilter, PostRepairWorkFilter, PostWalkingFilter, PostOrderFilter
from .forms import (PostOrderForm, PostRepairWorkForm, PostWalkingForm,
                    ResolutionForm)
from .logging import (log_post_walking_create, log_post_walking_edit, log_resolution_create,
                      log_resolution_edit, log_post_repair_work_create, log_post_repair_work_edit,
                      log_post_order_create, log_post_order_edit)
from .models import (Brigade, District, Personal, PostOrder, PostRepairWork,
                     PostWalking, Resolution)
from .services import view_resolution
from .tables import PersonalTable, PostOrderTable
from .validators import (CheckEnergyDistrictMixin,
                         get_filtered_energy_district,
                         validate_date_fields_post,
                         validate_fields_post_walking)
from .utils import get_breadcrumb_url


class HomePageView(TemplateView):
    template_name = 'office/index.html'


class CabinetView(LoginRequiredMixin, TemplateView):
    template_name = 'office/cabinet.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['breadcrumbs'] = {
            'url': get_breadcrumb_url(self.request.path), 
            'title_second': 'Кабинет',
        }
        return context


class JournalsListView(LoginRequiredMixin, TemplateView):
    template_name = 'office/journals.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['breadcrumbs'] = {
            'url': get_breadcrumb_url(self.request.path), 
            'title_second': 'Кабинет',
            'title_current': 'Журналы'
        }
        return context


class DistrictsListView(LoginRequiredMixin, ListView):
    model = District
    template_name = 'office/districts.html'
    context_object_name = 'districts'

    def get_queryset(self):
        return District.objects.filter(energy_district=self.request.user.energy_district)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['breadcrumbs'] = {
            'url': get_breadcrumb_url(self.request.path), 
            'title_second': 'Кабинет',
            'title_third': 'Журналы',
            'title_current': 'Журнал обходов тепловых сетей'
        }
        return context


class JournalWalkView(LoginRequiredMixin, CheckEnergyDistrictMixin, FilterView):
    model = PostWalking
    template_name = 'office/journal_walk.html'
    context_object_name = 'posts'
    filterset_class = PostWalkingFilter
    paginate_by = settings.AMOUNT_POSTS_WALK

    def get_queryset(self):
        district = get_object_or_404(District, slug=self.kwargs.get('slug_district'))
        return PostWalking.objects.filter(
            district=district).select_related('author', 'district').prefetch_related('members')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['district'] = get_object_or_404(District, slug=self.kwargs.get('slug_district'))

        context['title'] = 'Журнал обходов тепловых сетей'
        context['breadcrumbs'] = {
            'url': get_breadcrumb_url(self.request.path), 
            'title_second': 'Кабинет',
            'title_third': 'Журналы',
            'title_fourth': 'Журнал обходов тепловых сетей',
            'title_current': context['district'].title
        }
        return context


class PostWalkingCreateView(LoginRequiredMixin, CheckEnergyDistrictMixin, CreateView):
    model = PostWalking
    template_name = 'office/create_post_walking.html'
    form_class = PostWalkingForm

    def get_initial(self):
        initial = super().get_initial()
        initial['district'] = get_object_or_404(
            District, slug=self.kwargs.get('slug_district')
        )
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['link_back'] = reverse('office:journal_walk', kwargs={'slug_district': self.kwargs['slug_district']})

        return get_filtered_energy_district(self, context)

    def form_valid(self, form):
        form = validate_fields_post_walking(self, form)
        if form.errors:
            return self.form_invalid(form)
        post = form.save(commit=False)
        post.author = self.request.user
        post.save()
        return super().form_valid(form)

    def get_success_url(self):
        log_post_walking_create(post=self.object)

        messages.success(
            self.request, mark_safe(
                f'Запись № {self.object.number_post} успешно добавлена.'
                f' <a href="{self.object.id}/">Открыть запись</a>'
            )
        )
        return reverse('office:journal_walk', kwargs={
                 'slug_district': self.kwargs.get('slug_district'),
            })


class PostWalkingEditView(LoginRequiredMixin, CheckEnergyDistrictMixin, UpdateView):
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
                'office:districts',
            )
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['link_back'] = reverse('office:journal_walk', kwargs={'slug_district': context['object'].district.slug})

        return get_filtered_energy_district(self, context)

    def form_valid(self, form):
        form = validate_fields_post_walking(self, form)
        if form.errors:
            return self.form_invalid(form)
        post = form.save(commit=False)
        post.is_edit = True
        post.save()
        return super().form_valid(form)

    def get_success_url(self):
        log_post_walking_edit(post=self.object)

        messages.success(
            self.request, mark_safe(
                f'Запись № {self.object.number_post} успешно изменена.'
                f' <a href="{self.object.id}/">Открыть запись</a>'
            )
        )
        return reverse('office:journal_walk', kwargs={
                 'slug_district': self.kwargs.get('slug_district'),
            })


class PostWalkingDetailView(LoginRequiredMixin, CheckEnergyDistrictMixin, DetailView, FormView):
    model = PostWalking
    template_name = 'office/post_walking_detail.html'
    pk_url_kwarg = 'post_id'
    context_object_name = 'post'
    form_class = ResolutionForm

    def get_queryset(self):
        return super().get_queryset().select_related(
            'author', 'district')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['district'] = context['post'].district

        context['resolution'] = context['post'].resolution.first()
        if context['resolution'] and not context['resolution'].viewed and context['post'].author == self.request.user:
            view_resolution(resolution=context['resolution'])
            view_notification(post=context['post'])
            create_notification_view_resolution(resolution=context['resolution'], from_user=self.request.user)
        return context


class ResolutionAddView(LoginRequiredMixin, CheckEnergyDistrictMixin, CreateView):
    model = Resolution
    template_name = 'office/includes/resolution_form.html'
    fields = ['text']

    def form_valid(self, form):
        if self.request.user.is_staff:
            resolution = form.save(commit=False)
            resolution.author = self.request.user
            resolution.post_walking_id = self.kwargs.get('post_id')
            resolution.save()
            messages.success(self.request, 'Резолюция успешно добавлена.')

            log_resolution_create(resolution=resolution)

            create_notification(
                post_id=self.kwargs.get('post_id'),
                title='Новая резолюция',
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
                        self.kwargs.get('slug_district'),
                        self.kwargs.get('post_id')
                        )


class ResolutionEditView(LoginRequiredMixin, CheckEnergyDistrictMixin, UpdateView):
    model = Resolution
    fields = ['text']
    template_name = 'office/includes/resolution_update_form.html'
    pk_url_kwarg = 'resolution_id'

    def form_valid(self, form):
        messages.success(self.request, 'Резолюция успешно изменена.')
        log_resolution_edit(
            resolution=self.object,
            username=self.request.user.username
        )

        self.object.viewed = False

        create_notification(
            post_id=self.kwargs.get('post_id'),
            title='Измененная резолюция',
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

        context['breadcrumbs'] = {
            'url': get_breadcrumb_url(self.request.path), 
            'title_second': 'Бригады',
        }
        return context


class EmployeesListView(LoginRequiredMixin, SingleTableMixin, FilterView):
    model = Personal
    template_name = 'office/employees.html'
    context_object_name = 'employees'
    table_class = PersonalTable
    filterset_class = PersonalFilter

    def get_queryset(self):
        return Personal.objects.filter(
            energy_district=self.request.user.energy_district
            ).select_related('position')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['energy_district'] = self.request.user.energy_district

        context['breadcrumbs'] = {
            'url': get_breadcrumb_url(self.request.path), 
            'title_second': 'Сотрудники',
        }
        return context


class JournalRepairWorkView(LoginRequiredMixin, FilterView):
    model = PostRepairWork
    template_name = 'office/journal_repair_work.html'
    context_object_name = 'posts'
    filterset_class = PostRepairWorkFilter
    form_class = PostRepairWorkForm
    paginate_by = settings.AMOUNT_POSTS_REPAIR_WORK

    def get_queryset(self):
        return PostRepairWork.objects.filter(
            district__energy_district=self.request.user.energy_district
        ).select_related('author', 'district')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['energy_district'] = self.request.user.energy_district

        context['breadcrumbs'] = {
            'url': get_breadcrumb_url(self.request.path), 
            'title_second': 'Кабинет',
            'title_third': 'Журналы',
            'title_current': 'Журнал ремонтных работ'
        }
        return context


class PostRepairWorkCreateView(LoginRequiredMixin, CreateView):
    model = PostRepairWork
    template_name = 'office/create_post_repair.html'
    form_class = PostRepairWorkForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['link_back'] = reverse('office:journal_repair_work')

        return get_filtered_energy_district(self, context)

    def form_valid(self, form):
        form = validate_date_fields_post(self, form)
        if form.errors:
            return self.form_invalid(form)
        post = form.save(commit=False)
        post.author = self.request.user
        post.save()
        return super().form_valid(form)

    def get_success_url(self):
        log_post_repair_work_create(post=self.object)

        messages.success(
            self.request, mark_safe(
                f'Запись № {self.object.number_post} успешно добавлена.'
            )
        )
        return reverse('office:journal_repair_work')


class PostRepairWorkEditView(LoginRequiredMixin, UpdateView):
    model = PostRepairWork
    template_name = 'office/edit_post_repair.html'
    form_class = PostRepairWorkForm
    pk_url_kwarg = 'post_id'
    context_object_name = 'post'

    def dispatch(self, request, *args, **kwargs):
        post = self.get_object()
        if post.author != request.user:
            return redirect(
                'office:journal_repair_work',
            )
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['link_back'] = reverse('office:journal_repair_work')

        return get_filtered_energy_district(self, context)

    def form_valid(self, form):
        form = validate_date_fields_post(self, form)
        if form.errors:
            return self.form_invalid(form)
        post = form.save(commit=False)
        post.is_edit = True
        post.save()
        return super().form_valid(form)

    def get_success_url(self):
        log_post_repair_work_edit(post=self.object)

        messages.success(
            self.request, mark_safe(
                f'Запись № {self.object.number_post} успешно изменена.'
            )
        )
        return reverse('office:journal_repair_work')


class JournalOrderView(LoginRequiredMixin, SingleTableMixin, FilterView):
    model = PostOrder
    template_name = 'office/journal_order.html'
    context_object_name = 'posts'
    filterset_class = PostOrderFilter
    table_class = PostOrderTable
    paginate_by = settings.AMOUNT_POSTS_ORDER

    def get_queryset(self):
        return PostOrder.objects.filter(
            district__energy_district=self.request.user.energy_district
        ).select_related('author', 'district', 'foreman')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['energy_district'] = self.request.user.energy_district

        context['title'] = 'Журнал учета работ по нарядам и распоряжениям'
        context['breadcrumbs'] = {
            'url': get_breadcrumb_url(self.request.path), 
            'title_second': 'Кабинет',
            'title_third': 'Журналы',
            'title_current': 'Журнал учета работ по нарядам и распоряжениям'
        }
        return context


class PostOrderCreateView(LoginRequiredMixin, CreateView):
    model = PostOrder
    template_name = 'office/create_post_order.html'
    form_class = PostOrderForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['link_back'] = reverse('office:journal_order')

        return get_filtered_energy_district(self, context)

    def form_valid(self, form):
        form = validate_date_fields_post(self, form)
        if form.errors:
            return self.form_invalid(form)
        post = form.save(commit=False)
        post.author = self.request.user
        post.save()
        return super().form_valid(form)

    def get_success_url(self):
        log_post_order_create(post=self.object)

        messages.success(
            self.request, mark_safe(
                f'Запись № {self.object.number_post} ({self.object.order} № {self.object.number_order}) успешно добавлена.'
            )
        )
        return reverse('office:journal_order')


class PostOrderEditView(LoginRequiredMixin, UpdateView):
    model = PostOrder
    template_name = 'office/edit_post_order.html'
    form_class = PostOrderForm
    pk_url_kwarg = 'post_id'
    context_object_name = 'post'

    def dispatch(self, request, *args, **kwargs):
        post = self.get_object()
        if post.author != request.user:
            return redirect(
                'office:journal_order',
            )
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['link_back'] = reverse('office:journal_order')

        return get_filtered_energy_district(self, context)

    def form_valid(self, form):
        form = validate_date_fields_post(self, form)
        if form.errors:
            return self.form_invalid(form)
        post = form.save(commit=False)
        post.is_edit = True
        post.save()
        return super().form_valid(form)

    def get_success_url(self):
        log_post_order_edit(post=self.object)

        messages.success(
            self.request, mark_safe(
                f'Запись № {self.object.number_post} ({self.object.order} № {self.object.number_order}) успешно изменена.'
                f' <a href="edit-post-order/{self.object.id}/">Редактировать запись</a>'
            )
        )
        return reverse('office:journal_order')
