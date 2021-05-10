
import os
import re
import responses


class GlobalProxy:
    @staticmethod
    def enable(url):
        os.environ.update({
            'http_proxy': url,
            'https_proxy': url,
            'HTTP_PROXY': url,
            'HTTPS_PROXY': url
        })

    @staticmethod
    def disable(app):
        if 'http_proxy' in os.environ.keys():
            os.environ.pop('http_proxy')
        if 'https_proxy' in os.environ.keys():
            os.environ.pop('https_proxy')
        if 'HTTP_PROXY' in os.environ.keys():
            os.environ.pop('HTTP_PROXY')
        if 'HTTPS_PROXY' in os.environ.keys():
            os.environ.pop('HTTPS_PROXY')


class AzureInterceptor:
    HOSTS = [
        "https://management.azure.com",
        "https://login.microsoftonline.com"
    ]
    METHODS = ["GET", "PUT", "POST", "PATCH", "DELETE"]

    def __init__(self):
        self.http = responses.mock

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
        raise NotImplementedError('Subclass responsibility')
