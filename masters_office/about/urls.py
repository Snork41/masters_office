from django.urls import path

from . import views

app_name = 'about'

urlpatterns = [
    path('help/', views.HelpView.as_view(), name='help'),
    path('contacts/', views.ContactsView.as_view(), name='contacts'),
]
