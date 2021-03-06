import hashlib
import requests
import smtplib

from bostonGene.celery import app
from django.core.mail import send_mail
from md5_sum.models import Task

from bostonGene.settings import EMAIL_HOST_USER


def get_file_from_url(url):
    """ Generator that returns chunks of file from response."""
    try:
        req = requests.get(url, stream=True)
    except requests.ConnectionError:
        return
    if req.status_code == 200:
        for chunk in req.iter_content(1024):
            if not chunk:
                break
            yield chunk
    else:
        return


def get_md5_sum(hash_md5, chunk):
    """ Get md5 sum of byte string."""
    if hash_md5 is None:
        hash_md5 = hashlib.md5()
    hash_md5.update(chunk)
    return hash_md5


def send_email(email, task_id, status, hash_md5):
    """ Send email to current email."""
    try:
        send_mail('Md5_sum',
                  (f''' Task with id={task_id} has been completed.
                    This task has status: {status}.
                    md5_sum = {hash_md5}'''),
                  EMAIL_HOST_USER,
                  [email],
                  fail_silently=False,
                  )
    except smtplib.SMTPException as ex:
        print(ex.args)
        print('Message has not been sent.')


@app.task
def task_get_md5_hash(task_id, url, email):
    """ Performance of the task of getting md5 sum."""

    task = Task.objects.get(id=task_id)
    # Getting md5 sum of file.
    hash_md5 = None
    chunk_generator = get_file_from_url(url)

    # Check success of request.
    try:
        chunk = next(chunk_generator)
        hash_md5 = get_md5_sum(hash_md5=hash_md5, chunk=chunk)
    except StopIteration:
        chunk = False

    if chunk:
        for chunk in chunk_generator:
            hash_md5 = get_md5_sum(hash_md5=hash_md5, chunk=chunk)
        hash_md5 = hash_md5.hexdigest()
        task.md5_sum = hash_md5
        status = Task.DONE
        task.status = status
    else:
        status = Task.FAIL
        task.status = status
    task.save()

    # Sending email to user.
    if email:
        send_email(email, task_id, status, hash_md5)
