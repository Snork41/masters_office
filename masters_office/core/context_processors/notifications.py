from core.models import Notification


def check_new_resolutions(request):
    """Отвечает за уведомления."""
    if request.user.is_authenticated:
        unread_notifications = Notification.objects.filter(
            user=request.user,
            viewed=False
        )
        return {'notifications_count': unread_notifications.count(), 'notifications': unread_notifications}
    return {'notifications_count': 0}
