
import os


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
