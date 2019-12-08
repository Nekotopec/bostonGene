import pytest
from md5_sum.models import Task


@pytest.fixture(scope='session')
def celery_config():
    return {
        'broker_url': 'amqp://',
        'result_backend': 'rpc',
    }


@pytest.fixture(autouse=True)
def enable_db_access(db):
    pass


@pytest.fixture(scope='function')
def create_task(db):
    """ Fixture for creating task."""

    task = Task.objects.create(url='fff')
    yield task
    task.delete()


@pytest.fixture(scope='function')
def created_task(db):
    """ Create good task in database."""
    url = ('http://files.smashingmagazine.com/wallpapers/may-17/all-is-'
           'possible-in-may/nocal/may-17-all-is-possible-in-may-nocal-'
           '1920x1440.jpg?_ga=2.227303642.614725541.1575759309-'
           '1595750826.1575759309')
    task = Task.objects.create(url=url)
    yield task
    task.delete()


@pytest.fixture(scope='function')
def bad_task(db):
    """ Create bad task with nonexistent url."""
    url = 'http://some/bad/url/tralalal'
    task = Task.objects.create(url=url)

    yield task

    task.delete()