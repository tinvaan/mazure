
import functools

from .proxy import Mazure
from .services import app, services
from .services.utils import endpoints, register


def mazure(*fargs, **fkwargs):
    def interface(func):
        @functools.wraps(func)
        def action(*args, **kwargs):
            with Mazure():
                func(*args, **kwargs)
        return action

    api_version = app.config.get('AZURE_API_VERSION')
    allow_live = app.config.get('ALLOW_AZURE_REQUESTS')
    app.config.update({
        'AZURE_API_VERSION': fkwargs.get('version', api_version),
        'ALLOW_AZURE_REQUESTS': fkwargs.get('allow', allow_live)
    })
    register(app, list(endpoints(fargs, services)))
    return interface
