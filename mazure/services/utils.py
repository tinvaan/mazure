
from flask import Blueprint
from inspect import isfunction
from importlib import import_module

from .exceptions import NotSupported


def bp(app, modname, anchor):
    """
    Returns the Flask blueprint object for a service
    """
    with app.app_context():
        mod = import_module('.%s.views' % modname, anchor)
        for name in dir(mod):
            attr = getattr(mod, name)
            if isinstance(attr, Blueprint):
                return attr


def combine(services):
    """
    Returns a combined list of azure component and property strings
    """
    components = list(services.keys())
    properties = list(
        service.property for service in sum(services.values(), list())
    )
    return sum([components, properties], list())


def endpoints(args, services):
    """
    Returns all endpoints that need to be registered,
    based on a user's decorator usage.
    """
    result = list()
    names = combine(services)
    supported = sum(services.values(), list())
    targets = [arg for arg in args if not isfunction(arg)]

    if len(targets) == 0:
        return supported

    if not set(targets).issubset(set(names)):
        raise NotSupported(set(targets).difference(set(names)))

    for target in targets:
        if target not in services.keys():
            for service in supported:
                if service.property == target:
                    result.append(service)
        else:
            return services.get(target)
    return result


def register(app, targets):
    """
    Registers the requested set of services onto the main Flask object
    """
    with app.app_context():
        for service in targets:
            if not service.prefix:
                app.register_blueprint(service.blueprint)
            else:
                app.register_blueprint(
                    service.blueprint, url_prefix=service.prefix)
