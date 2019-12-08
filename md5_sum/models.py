from django.db import models
import uuid


# Create your models here.


class Task(models.Model):
    """ Model of task."""

    DONE = 'Done'
    IN_PROGRESS = 'in progress'
    FAIL = 'fail'
    NOT_EXIST = 'not exist'

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    url = models.URLField()
    email = models.EmailField(null=True)
    md5_sum = models.TextField(blank=True)
    status = models.CharField(
        max_length=30,
        choices=[(DONE, 'The task is completed.'),
                 (IN_PROGRESS, 'The task is in progress.'),
                 (FAIL, 'The task is failed.'),
                 (NOT_EXIST, 'The task does not exist.')],
        default=IN_PROGRESS,
    )

    def __str__(self):
        return f'id:\t {self.id},\nemail:\t {self.email},\nurl:\t {self.url}'
