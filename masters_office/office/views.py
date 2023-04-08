from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, TemplateView

from .models import District, User, Journal, PostWalking
from .forms import PostWalkingForm


class Index(TemplateView):
    template_name = 'office/index.html'


def index(request):
    context = {}
    return render(request, 'office/index.html', context)


@login_required
def cabinet(request, username):
    master = get_object_or_404(User, username=username)
    context = {
        'master': master,
    }
    return render(request, 'office/cabinet.html', context)


@login_required
def districts_list(request, username, slug_journal):
    districts = District.objects.all()
    journal = get_object_or_404(Journal, slug=slug_journal)
    master = get_object_or_404(User, username=username)
    context = {
        'districts': districts,
        'journal': journal,
        'master': master,
    }
    return render(request, 'office/districts.html', context)


@login_required
def journals_list(request, username):
    all_journals = Journal.objects.all()
    context = {
        'all_journals': all_journals,
    }
    return render(request, 'office/journals.html', context)


@login_required
def journal_walk(request, username, slug_journal, slug_district):
    district = get_object_or_404(District, slug=slug_district)
    posts = PostWalking.objects.filter(district_id=district.id)
    master = get_object_or_404(User, username=username)
    journal = get_object_or_404(Journal, slug=slug_journal)
    context = {
        'posts': posts,
        'district': district,
        'master': master,
        'journal': journal,
    }
    return render(request, 'office/journal_walk.html', context)


@login_required
def create_post_walking(request, username, slug_journal, slug_district):
    district = get_object_or_404(District, slug=slug_district)
    initial_data = {'district': district,}
    form = PostWalkingForm(
        request.POST or None,
        files=request.FILES or None,
        initial = initial_data,
    )
    context = {
        'form': form,
    }
    if form.is_valid():
        form.save(request.user)
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
    fields_hidden.widget =  fields_hidden.hidden_widget()
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


@login_required
def post_detail(request, username, slug_journal, slug_district, post_id):
    post = get_object_or_404(PostWalking, id=post_id)
    district = get_object_or_404(District, slug=slug_district)
    master = get_object_or_404(User, username=username)
    journal = get_object_or_404(Journal, slug=slug_journal)
    context = {
        'post': post,
        'district': district,
        'master': master,
        'journal': journal,
    }
    return render(request, 'office/post_walking_detail.html', context)
