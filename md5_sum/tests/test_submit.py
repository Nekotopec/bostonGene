from md5_sum.tasks import task_get_md5_hash


# Create your tests here.


class TestSubmit:
    def test_good_request(self, client, monkeypatch):
        """ Test api method submit with good request."""
        form_data = {
            'url': ('https://sun9-45.userapi.com/c850036/'
                    'v850036852/140d68/gfncjqv-qnA.jpg'),
        }
        monkeypatch.setattr(
            task_get_md5_hash, 'delay', lambda *args: None,
        )
        response = client.post('http://127.0.0.1:8000/submit/',
                               data=form_data)
        assert response.status_code == 200

    def test_bad_request(self, client):
        """ Test api method submit with bad request."""

        # Request with empty url
        form_data = {
            'url': ''
        }
        response = client.post('http://127.0.0.1:8000/submit/',
                               data=form_data)

        assert response.status_code == 400

    def test_request_without_url(self, client):
        """ Test api method submit with request without required parameters."""

        form_data = dict()
        response = client.post('http://127.0.0.1:8000/submit/',
                               data=form_data)

        assert response.status_code == 400
