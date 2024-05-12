from core.models import Notification
from office.models import PostWalking


def create_notification(post_id: int, title: str) -> None:
    """Создание нового уведомления"""
    post = PostWalking.objects.get(id=post_id)
    content_dict = {
        'Новая резолюция': f'Добавлена новая резолюция к {post} ({post.district})',
        'Измененная резолюция': f'Изменена резолюция к {post} ({post.district})'
    }

    Notification.objects.create(
        user=post.author,
        title=title,
        content=content_dict[title],
        link=post.get_absolute_url()
    )


def view_notification(post=None, notification_id=None) -> None:
    """Смена статуса уведомления на просмотрено"""
    if notification_id:
        Notification.objects.filter(
            id=notification_id
        ).update(viewed=True)
    else:
        Notification.objects.filter(
            link=post.get_absolute_url()
        ).update(viewed=True)


def create_notification_view_resolution(resolution, from_user) -> None:
    """Создание уведомления о просмотре резолюции"""
    Notification.objects.create(
        user=resolution.author,
        title='Просмотрена резолюция',
        content=f'Пользователь {from_user.username.upper()} просмотрел вашу резолюцию на {resolution.post_walking}',
    )
