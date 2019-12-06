from django.test import TestCase, override_settings
from unittest.mock import patch
import pytest
import requests


# Create your tests here.


class TestSubmit:

    def test_good_request(self):
        """ Test api method submit with good request."""
        form_data = {
            'url': ('https://sun9-45.userapi.com/c850036/'
                    'v850036852/140d68/gfncjqv-qnA.jpg'),
        }

        response = requests.post('http://127.0.0.1:8000/submit/',
                                 data=form_data)

        assert response.status_code == 200

    def test_bad_request(self):
        """ Test api method submit with bad request."""
        # Request with empty url
        form_data = {
            'url': ''
        }
        response = requests.post('http://127.0.0.1:8000/submit/',
                                 data=form_data)

        assert response.status_code == 400

    def test_request_without_url(self):
        """ Test api method submit with request without required parameters."""
        form_data = dict()
        response = requests.post('http://127.0.0.1:8000/submit/',
                                 )
        assert response.status_code == 400
