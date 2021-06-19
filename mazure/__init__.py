
import inspect
import functools

from .services import app
from .proxy import Mazure


services = dict(
    compute=['virtual_machines'],
    storage=['storage_accounts']
)


def supported(target):
    if str(target).lower() not in services.keys():
        properties = list()
        for names in services.values():
            properties.extend(names)
        return str(target).lower() in set(properties)
    return True


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
    for target in fargs:
        if not inspect.isfunction(target):
            assert supported(target), """
            Support for the '%s' service is unavailable in the current release.
            Please check the latest release, or file a support request at '%s'
            """ % (target, "https://github.com/tinvaan/mazure/issues")

    return interface
