from md5_sum.tasks import task_get_md5_hash
from md5_sum.models import Task


class TestTasks:
    """ Class to test tasks performance."""

    def test_task_with_good_url(self, created_task, patch_request):
        patch_request()
        """ Test performance of good task."""
        task_id = created_task.id
        task_url = created_task.url
        task_email = None
        task_get_md5_hash(task_id, task_url, task_email)

        # Getting Task object to check completion
        completed_task = Task.objects.get(id=task_id)
        assert completed_task.status == 'Done'

    def test_task_failure(self, bad_task, patch_request):
        """ Try to get md5 sum from url that does not exist."""
        patch_request(404)

        task_id = bad_task.id
        task_url = bad_task.url
        task_email = None
        task_get_md5_hash(task_id, task_url, task_email)

        # Getting Task object to check completion
        completed_task = Task.objects.get(id=task_id)
        assert completed_task.status == Task.FAIL

    def test_correctness_of_md5_sum(self, created_task, patch_request):
        """ Test correctness of the calculation md5 sum."""
        patch_request()

        correct_md5_sum = '284ffcb6fcfab009ea3aa57bace6b1b4'
        task_id = created_task.id
        task_url = created_task.url
        task_email = None
        task_get_md5_hash(task_id, task_url, task_email)

        # Getting Task object to check completion
        completed_task = Task.objects.get(id=task_id)

        assert completed_task.md5_sum == correct_md5_sum


