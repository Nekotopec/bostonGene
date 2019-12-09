from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from md5_sum.models import Task
from .tasks import task_get_md5_hash
from django.core.exceptions import ValidationError


@require_http_methods(["GET"])
def check(request):
    """ Check status of task completion."""

    id = request.GET.get('id')
    if id:

        try:
            task = Task.objects.get(id=id)
        except Task.DoesNotExist:
            data = {'status': 404,
                    'message': f'Task with id={id} does not exist.'}
            return JsonResponse(data=data,
                                status=404)
        except ValidationError:
            data = {'status': 400,
                    'message': f'Id={id} is not a valid UUID.'}
            return JsonResponse(data=data,
                                status=400)

        status = task.status
        if status == Task.DONE:
            return JsonResponse(data={
                'md5': task.md5_sum,
                'status': status,
                'url': task.url
            })
        else:
            return JsonResponse(data={
                'status': status,
            })
    else:
        return JsonResponse(data={'status': 400,
                                  'message': 'Bad parameters'}, status=400)


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

