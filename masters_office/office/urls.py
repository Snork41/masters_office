from django.urls import path, re_path
from django import views as django_views

from . import views

app_name = 'office'

urlpatterns = [
    path('', views.index, name='index'),
    re_path(r'^jsi18n/$', django_views.i18n.JavaScriptCatalog.as_view(), name='jsi18n'),
    path('cabinet/<str:username>/', views.cabinet, name='cabinet'),
    path('cabinet/<str:username>/journals/', views.journals_list, name='journals'),
    path('cabinet/<str:username>/journals/<slug:slug_journal>/districts/', views.districts_list, name='districts'),
    path('cabinet/<str:username>/journals/<slug:slug_journal>/districts/<slug:slug_district>/', views.journal_walk, name='journal_walk'),
    path('cabinet/<str:username>/journals/<slug:slug_journal>/districts/<slug:slug_district>/create-post-walking/', views.create_post_walking, name='create_post_walking'),
    path('cabinet/<str:username>/journals/<slug:slug_journal>/districts/<slug:slug_district>/<int:post_id>/edit-post-walking/', views.edit_post_walking, name='edit_post_walking'),
    path('cabinet/<str:username>/journals/<slug:slug_journal>/districts/<slug:slug_district>/<int:post_id>/', views.post_detail, name='post_walking_detail'),
    path('cabinet/<str:username>/journals/<slug:slug_journal>/districts/<slug:slug_district>/<int:post_id>/resolution/', views.add_resolution, name='add_resolution'),
    path('cabinet/<str:username>/journals/<slug:slug_journal>/districts/<slug:slug_district>/<int:post_id>/edit_resolution/', views.edit_resolution, name='edit_resolution'),
]
