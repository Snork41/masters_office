from django.urls import path, re_path
from django import views as django_views

from . import views

app_name = 'office'

urlpatterns = [
    path('', views.HomePageView.as_view(), name='index'),
    re_path(r'^jsi18n/$',
            django_views.i18n.JavaScriptCatalog.as_view(), name='jsi18n'),
    path('cabinet/',
         views.CabinetView.as_view(), name='cabinet'),
    path(
        'cabinet/journals/',
        views.JournalsListView.as_view(), name='journals'),
    path(
        'cabinet/journals/<slug:slug_journal>/districts/',
        views.DistrictsListView.as_view(), name='districts'),
    path(
        'cabinet/journals/<slug:slug_journal>/districts/<slug:slug_district>/',
        views.JournalWalkView.as_view(), name='journal_walk'),
    path(
        'cabinet/journals/<slug:slug_journal>/districts/<slug:slug_district>/create-post-walking/',
        views.PostWalkingCreateView.as_view(), name='create_post_walking'),
    path(
        'cabinet/journals/<slug:slug_journal>/districts/<slug:slug_district>/edit_post_walking/<int:post_id>/',
        views.PostWalkingEditView.as_view(), name='edit_post_walking'),
    path(
        'cabinet/journals/<slug:slug_journal>/districts/<slug:slug_district>/<int:post_id>/',
        views.PostWalkingDetailView.as_view(), name='post_walking_detail'),
    path(
        'cabinet/journals/<slug:slug_journal>/districts/<slug:slug_district>/<int:post_id>/resolution/',
        views.ResolutionAddView.as_view(), name='resolution_form'),
    path(
        'cabinet/journals/<slug:slug_journal>/districts/<slug:slug_district>/<int:post_id>/resolution/<pk>/',
        views.ResolutionEditView.as_view(), name='resolution_update_form'),
]
