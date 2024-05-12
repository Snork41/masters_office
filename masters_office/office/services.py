from office.models import Resolution


def view_resolution(resolution) -> None:
    """Смена статуса резолюции на просмотрено"""
    Resolution.objects.filter(
        id=resolution.id
    ).update(viewed=True)
