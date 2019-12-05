import hashlib
import requests
import smtplib

from boston_gene.celery import app
from django.core.mail import send_mail
from submit.models import Task


def get_file_from_url(url):
    """ Generator that returns chunks of file from response."""
    req = requests.get(url, stream=True)
    if req.status_code == 200:
        for chunk in req.iter_content(1024):
            yield chunk
    else:
        return False


def get_md5_sum(hash_md5, chunk):
    """ Get md5 sum of byte string."""
    if hash_md5 is None:
        hash_md5 = hashlib.md5()
    hash_md5.update(chunk)
    return hash_md5


@app.task
def task_get_md5_hash(task_id):
    """ Performance of the task of getting md5 sum."""
    task = Task.objects.get(id=task_id)

    # Getting md5 sum of file.
    hash_md5 = None
    chunk_generator = get_file_from_url(task.url)
    if chunk_generator:
        for chunk in chunk_generator:
            hash_md5 = get_md5_sum(hash_md5=hash_md5, chunk=chunk)
        task.md5_sum = hash_md5
        task.status = Task.DONE
    else:
        task.status = Task.FAIL
    task.save()

    # Sending email to user.

    # TODO: Доделать мыло
    if task.email:
        try:
            send_mail('Md5_sum',
                      (f'Task with id={task.id} '
                       f'has been completed'
                       f'md5_sum = {task.md5_sum}'))
        except smtplib.SMTPException:
            print('Message has not been sent.')
