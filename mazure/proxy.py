
import re
import json
import requests

from urllib.parse import urlparse
from werkzeug.exceptions import NotFound

from packages import responses

from .services import app
from .services.exceptions import NotSupported
from .services.utils import services, register


class Mazure:
    HOSTS = [
        "https://management.azure.com",
        "https://login.microsoftonline.com",
        "https://(.*\.)?documents.azure.com"
    ]
    METHODS = ["HEAD", "GET", "PUT", "POST", "PATCH", "DELETE"]

    def __init__(self, targets=[], allow=None):
        self.targets = targets
        self.allow = allow or app.config.get('ALLOW_AZURE_REQUESTS')
        app.config.update({'ALLOW_AZURE_REQUESTS': self.allow})

        self.http = responses.mock
        self.client = app.test_client()
        self.host = 'http://%s:%s' % (
            app.config.get('MAZURE_SERVER'), app.config.get('MAZURE_PORT'))

    def __enter__(self, *args, **kwargs):
        self.allow = kwargs.get(
            'allow', app.config.get('ALLOW_AZURE_REQUESTS'))
        app.config.update({'ALLOW_AZURE_REQUESTS': self.allow})
        register(app, services(app, self.targets))
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

    def routable(self, path, method):
        try:
            return app.url_map.bind(app.config.get('MAZURE_SERVER'))\
                              .match(path, method) is not None
        except NotFound:
            return False

    def callback(self, request):
        if not self.routable(urlparse(request.url).path, request.method):
            if self.allow:
                self.http.add_passthru(request.url)
                r = requests.session().send(request)
                return (r.status_code, dict(r.headers), r.content)
            raise NotSupported('"%s" is not supported' % request.url)

        response = getattr(self.client, request.method.lower())(
            self.host + request.path_url, data=request.body)
        return (
            response.status_code,
            dict(response.headers),
            json.dumps(response.get_json()) if response.data else response.data
        )
