
import inspect
import functools

from .services import app
from .proxy import Mazure


def mazure(*fargs, **fkwargs):
    def interface(func):
        @functools.wraps(func)
        def action(*args, **kwargs):
            with Mazure(targets):
                func(*args, **kwargs)
        return action

    api_version = app.config.get('AZURE_API_VERSION')
    allow_live = app.config.get('ALLOW_AZURE_REQUESTS')
    app.config.update({
        'AZURE_API_VERSION': fkwargs.get('version', api_version),
        'ALLOW_AZURE_REQUESTS': fkwargs.get('allow', allow_live)
    })
    targets = [arg for arg in fargs if not inspect.isfunction(arg)]
    return interface
