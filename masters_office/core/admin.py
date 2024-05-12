from django.contrib import admin

from simple_history.admin import SimpleHistoryAdmin

from .models import Notification


@admin.register(Notification)
class NotificationAdmin(SimpleHistoryAdmin):
    list_display = (
        'id',
        'user',
        'title',
        'content',
        'viewed',
        'time_create',
    )
    list_filter = ('user', 'viewed',)
