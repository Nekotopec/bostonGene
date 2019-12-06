from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from submit.models import Task
from django.core.exceptions import ObjectDoesNotExist


@require_http_methods(["GET"])
def check(request):
    """ Check status of task completion"""
    id = request.GET.get('id')
    print(id)
    if id:
        try:
            task = Task.objects.get(id=id)
        except ObjectDoesNotExist:
            return JsonResponse(data={'status': 404,
                               'message': f'Task with id={id} does not exist.'}, status=400)
        if task:
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
