from md5_sum.tasks import task_get_md5_hash
from md5_sum.models import Task

class TestTasks:
    """ Class to test tasks performance."""

    def test_task_with_good_url(self, created_task):
        """ Test performance of good task."""
        task_id = created_task.id
        task_url = created_task.url
        task_email = None
        task_get_md5_hash.apply(args=(task_id, task_url, task_email))

        # Getting Task object to check completion
        completed_task = Task.objects.get(id=task_id)
        assert completed_task.status == 'Done'

    def test_task_failure(self, bad_task):
        """ Try to get md5 sum from url that does not exist."""
        task_id = bad_task.id
        task_url = bad_task.url
        task_email = None
        task_get_md5_hash.apply(args=(task_id, task_url, task_email))

        # Getting Task object to check completion
        completed_task = Task.objects.get(id=task_id)
        assert completed_task.status == Task.FAIL

    def test_correctness_of_md5_sum(self, created_task):
        """ Test correctness of the calculation md5 sum."""
        correct_md5_sum =  'c7bc71907fee313afacdc0946619d13c'
        task_id = created_task.id
        task_url = created_task.url
        task_email = None
        task_get_md5_hash.apply(args=(task_id, task_url, task_email))

        # Getting Task object to check completion
        completed_task = Task.objects.get(id=task_id)

        assert completed_task.md5_sum == correct_md5_sum
