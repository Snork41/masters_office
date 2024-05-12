from django.urls import path

from .views import view_notification_ajax

app_name = 'core'

urlpatterns = [
    path('view_notification/', view_notification_ajax, name='view_notification'),
]
