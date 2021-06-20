
from flask import Blueprint
from importlib import import_module

from .exceptions import NotSupported


def combine(app):
    """
    Returns a combined list of azure component and property strings
    """
    components = list(app.config.get('services').keys())
    properties = list(
        service.property
        for service in sum(app.config.get('services').values(), list())
    )
    return sum([components, properties], list())


def services(app, args):
    """
    Returns all services that need to be registered,
    based on a user's decorator usage.
    """
    names = combine(app)
    result = list(app.config.get('services').get('auth'))
    supported = sum(app.config.get('services').values(), list())

    if len(args) == 0:
        return supported

    if not set(args).issubset(set(names)):
        raise NotSupported(set(args).difference(set(names)))

    for name in args:
        if name not in app.config.get('services').keys():
            for service in supported:
                if service.property == name:
                    result.append(service)
        else:
            result.extend(app.config.get('services').get(name))
    return result


def register(app, services):
    """
    Registers the requested set of services onto the main Flask object
    """
    with app.app_context():
        for service in services:
            if not service.prefix:
                app.register_blueprint(service.blueprint)
            else:
                app.register_blueprint(
                    service.blueprint, url_prefix=service.prefix)


def blueprint(app, modname, anchor=".".join(__name__.split('.')[:-1])):
    """
    Returns the Flask blueprint object for a service
    """
    with app.app_context():
        mod = import_module('.%s.views' % modname, anchor)
        for name in dir(mod):
            attr = getattr(mod, name)
            if isinstance(attr, Blueprint):
                return attr
