import pytest


class TestCheck:

    def test_good_request(self, client, create_task):
        """ Testing good request to check method."""

        task = create_task
        response = client.get(
            f'http://127.0.0.1:8000/check/?id={task.id}').json()
        print(response['status'])
        assert response['status'] == task.status

    def test_get_nonexistent_task(self, client):
        """ Try to get task nonexistent task.
        Expect 404 status code
        """

        nonexistent_id = '0e4fac17-f367-4807-8c28-8a059a2f82ac'
        url = f'http://127.0.0.1:8000/check/?id={nonexistent_id}'
        response = client.get(url)
        assert response.status_code == 404

    def test_bad_parameters(self, client):
        """ Try to do request with bad parameters."""

        response = client.get('http://127.0.0.1:8000/check/?kekv=lalalal')
        assert response.status_code == 400



