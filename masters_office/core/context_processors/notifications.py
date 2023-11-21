from office.models import Resolution


def check_new_resolutions(request):
    """Отвечает за уведомления."""
    if request.user.is_authenticated:
        unread_notifications = Resolution.objects.filter(
            post_walking__district__master=request.user,
            viewed=False).select_related('post_walking', 'post_walking__district')
        return {'notifications_count': unread_notifications.count(), 'notifications': unread_notifications}
    return {'notifications_count': 0}
