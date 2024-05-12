import logging

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .services import view_notification

logger = logging.getLogger('django.request')


def page_not_found(request, exception):
    return render(request, 'core/404.html', {'path': request.path}, status=404)


def csrf_failure(request, reason=''):
    return render(request, 'core/403csrf.html')


@csrf_exempt
@require_POST
def view_notification_ajax(request):
    try:
        view_notification(notification_id=int(request.POST.get('id')))
    except Exception as err:
        return JsonResponse({"status": "error", "message": "Не удалось выполнить действие"}, status=404)
    return JsonResponse({'status': 'success'}, status=200)
