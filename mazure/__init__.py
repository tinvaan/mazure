
import functools

from .proxy import Mazure


def mazure(func):
    @functools.wraps(func)
    def interface(*args, **kwargs):
        with Mazure():
            func(*args, **kwargs)
    return interface
