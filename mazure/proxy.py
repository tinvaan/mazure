
import re
import json
import responses
import functools

from .services import app


class AzureProxy:
    HOSTS = [
        "https://management.azure.com",
        "https://login.microsoftonline.com"
    ]
    METHODS = ["GET", "PUT", "POST", "PATCH", "DELETE"]

    def __init__(self):
        self.http = responses.mock
        self.client = app.test_client()
        self.host = 'http://%s:%s' % (
            app.config.get('MAZURE_SERVER'), app.config.get('MAZURE_PORT'))

    def __enter__(self, *args, **kwargs):
        self.setup()

    def __exit__(self, *args, **kwargs):
        self.cleanup()

    def setup(self):
        self.http.start()
        for method in self.METHODS:
            for host in self.HOSTS:
                self.http.add_callback(
                    method,
                    re.compile(host),
                    callback=self.callback,
                    content_type='application/json')

    def cleanup(self):
        self.http.stop()
        self.http.reset()

    def callback(self, request):
        if request.method == 'GET':
            response = self.client.get(self.host + request.path_url)
        if request.method == 'DELETE':
            response = self.client.delete(self.host + request.path_url)
        if request.method == 'POST':
            response = self.client.post(
                self.host + request.path_url, data=request.body)
        if request.method == 'PUT':
            response = self.client.put(
                self.host + request.path_url, data=request.body)

        return (
            response.status_code,
            dict(response.headers),
            json.dumps(response.get_json())
        )


def mazure(func):
    @functools.wraps(func)
    def interface(*args, **kwargs):
        with AzureProxy():
            func(*args, **kwargs)
    return interface
