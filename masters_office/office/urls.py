from django.urls import path

from . import views

app_name = 'office'

urlpatterns = [
    path('', views.index, name='index'),
    path('cabinet/<str:username>/', views.cabinet, name='cabinet'),
    path('cabinet/<str:username>/journals/', views.journals_list, name='journals'),
    path('cabinet/<str:username>/journals/<slug:slug_journal>/districts/', views.districts_list, name='districts'),
    path('cabinet/<str:username>/journals/<slug:slug_journal>/districts/<slug:slug_district>/', views.journal_walk, name='journal_walk'),
    path('cabinet/<str:username>/journals/<slug:slug_journal>/districts/<slug:slug_district>/create-post-walking/', views.create_post_walking, name='create_post_walking'),
    path('cabinet/<str:username>/journals/<slug:slug_journal>/districts/<slug:slug_district>/<int:post_id>/edit-post-walking/', views.edit_post_walking, name='edit_post_walking'),
    path('cabinet/<str:username>/journals/<slug:slug_journal>/districts/<slug:slug_district>/<int:post_id>/', views.post_detail, name='post_walking_detail'),
]
