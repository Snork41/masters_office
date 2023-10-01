from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, TemplateView, DetailView, FormView, CreateView


from .models import District, Journal, PostWalking, Resolution
from .forms import PostWalkingForm, ResolutionForm


class HomePage(TemplateView):
    template_name = 'office/index.html'


class Cabinet(LoginRequiredMixin, TemplateView):
    template_name = 'office/cabinet.html'


class JournalsList(LoginRequiredMixin, ListView):
    model = Journal
    template_name = 'office/journals.html'
    context_object_name = 'all_journals'


class DistrictsList(LoginRequiredMixin, ListView):
    model = District
    template_name = 'office/districts.html'
    context_object_name = 'districts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['journal'] = get_object_or_404(Journal, slug=self.kwargs.get('slug_journal'))
        return context


class JournalWalk(LoginRequiredMixin, ListView):
    model = Journal
    template_name = 'office/journal_walk.html'
    context_object_name = 'journal'

    def get_queryset(self):
        return get_object_or_404(Journal, slug=self.kwargs.get('slug_journal'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['district'] = get_object_or_404(District, slug=self.kwargs.get('slug_district'))
        context['posts'] = context['journal'].posts.filter(district_id=context['district'].id)
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
        return redirect('office:journal_walk', username, slug_journal, slug_district)
    return render(request, 'office/create_post_walking.html', context)


@login_required
def edit_post_walking(request, username, slug_journal, slug_district, post_id):
    post = get_object_or_404(PostWalking, id=post_id)

    if post.author != request.user:
        return redirect('office:post_walking_detail', username, slug_journal, slug_district, post_id)
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
            return redirect('office:post_walking_detail', username, slug_journal, slug_district, post_id)
    return render(request, 'office/create_post_walking.html', context)


class PostWalkingDetail(LoginRequiredMixin, DetailView, FormView):
    model = PostWalking
    template_name = 'office/post_walking_detail.html'
    pk_url_kwarg = 'post_id'
    context_object_name = 'post'
    form_class = ResolutionForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['district'] = context['post'].district
        context['journal'] = context['post'].journal
        context['resolution'] = context['post'].resolution.first()
        return context
    

class ResolutionAdd(LoginRequiredMixin, CreateView):
    form_class = ResolutionForm

    def form_valid(self, form):
        if self.request.user.is_staff:
            resolution = form.save(commit=False)
            resolution.author = self.request.user
            resolution.post_walking_id = self.kwargs.get('post_id')
            resolution.save()
            messages.success(self.request, 'Резолюция успешно добавлена')
            return super().form_valid(form)
        return self.form_invalid(form=form, message=True)
    
    def form_invalid(self, form, message=False):
        if message:
            messages.warning(self.request, 'Резолюцию может оставлять только Начальник')
        else:
            messages.warning(self.request, 'Резолюция не может быть пустой')
        return redirect('office:post_walking_detail',
                        self.kwargs.get('username'),
                        self.kwargs.get('slug_journal'),
                        self.kwargs.get('slug_district'),
                        self.kwargs.get('post_id')
                        )


@login_required
def edit_resolution(request, username, slug_journal, slug_district, post_id):
    resolution = get_object_or_404(Resolution, post_walking_id=post_id)

    if resolution.author != request.user:
        return redirect('office:post_walking_detail', username, slug_journal, slug_district, post_id)

    form = ResolutionForm(
        request.POST or None,
        files=request.FILES or None,
        instance=resolution,
    )

    if form.is_valid():
        form.save(request.user)
        messages.success(request, 'Резолюция успешно изменена')
    return redirect('office:post_walking_detail', username, slug_journal, slug_district, post_id)
