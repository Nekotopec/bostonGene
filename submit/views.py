from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import Task
from .tasks import task_get_md5_hash
from django.views import View


@require_http_methods(["POST"])
@csrf_exempt
def submit(request):
    """ View to submit task."""
    url = request.POST.get('url')
    email = request.POST.get('email')
    if not url:
        return JsonResponse(data={'status': 400,
                                  'message': 'Bad parameters'}, status=400)
    else:
        task = Task.objects.create(url=url, email=email)
        task_get_md5_hash.delay(task.id, url, email)
        return JsonResponse({'id': task.id})
