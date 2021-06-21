
import inspect
import functools

from .proxy import Mazure


def mazure(*fargs, **fkwargs):
    def interface(func):
        @functools.wraps(func)
        def action(*args, **kwargs):
            with Mazure(targets, fkwargs.get('allow')):
                func(*args, **kwargs)
        return action

    targets = [arg for arg in fargs if not inspect.isfunction(arg)]
    return interface
