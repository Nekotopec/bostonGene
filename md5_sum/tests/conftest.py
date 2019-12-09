import os
import requests
import pytest
from md5_sum.models import Task


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


@pytest.fixture(scope='function')
def patch_request(monkeypatch):
    class MockResponse:
        def __init__(self, status_code):
            self.status_code = status_code

        @staticmethod
        def iter_content(chunk_size):
            image_path = os.path.join(
                os.path.dirname(__file__),
                'static/kitty.jpg',
            )
            with open(image_path, 'rb') as f:
                while True:
                    data = f.read(chunk_size)
                    if not data:
                        break
                    yield data

    def _wrap(status=200):

        def mock_get(*args, **kwargs):
            return MockResponse(status)

        monkeypatch.setattr(requests, 'get', mock_get)

    yield _wrap
