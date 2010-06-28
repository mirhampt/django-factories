from django.db.models import get_model
from functools import wraps
import re


__all__ = ['Factory', 'blueprint']


class FactoryMetaclass(type):
    def __new__(meta, classname, bases, class_dict):
        new_methods = {}

        # Find all of the blueprints.
        for key, val in class_dict.iteritems():
            if hasattr(val, '_factories_blueprint') and callable(val):
                # Found a blueprint, create a 'build_' and 'create_' method for
                # it.
                def _make_method(save=False):
                    def _build_method(self, blueprint=val, model_cls=val._factories_model, **kwargs):
                        properties = blueprint(self)
                        properties.update(kwargs)

                        # Interpolate property values into strings.
                        for property in properties:
                            if isinstance(properties[property], basestring):
                                properties[property] = properties[property] % properties

                        # Create the instance of the model and maybe save it.
                        instance = model_cls(**properties)
                        if save:
                            instance.save()
                        return instance

                    # Set the docstring for the new method.
                    if save:
                        _build_method.__doc__ = "Create and save an instance of the '%s' model based on the '%s' blueprint." % (val._factories_model.__name__, key)
                    else:
                        _build_method.__doc__ = "Create but do not save an instance of the '%s' model based on the '%s' blueprint." % (val._factories_model.__name__, key)

                    return _build_method

                new_methods['build_' + key] = _make_method()
                new_methods['create_' + key] = _make_method(save=True)

        class_dict.update(new_methods)
        return type.__new__(meta, classname, bases, class_dict)


class Factory(object):
    """
    Baseclass for model factories.
    """
    __metaclass__ = FactoryMetaclass


def blueprint(model):
    """
    Decorator to mark a method as a factory blueprint.

    There is one required argument::

        model
            This specifies the model that corresponds with this blueprint.  It
            should be a string with the format: 'app_name.ModelName'.  This app
            will need to appear in INSTALLED_APPS in your project settings.

    Usage::

        @blueprint(model='auth.User')
        def basic_user():
            "Create a minimal User."
            return {
                'first_name': 'John',
                'last_name': 'Doe',
            }

    """
    def _decorator(func):
        @wraps(func)
        def _wrapped_func(*args, **kwargs):
            return func(*args, **kwargs)

        # Get the model class from the ``model`` string.
        try:
            app_name, model_name = model.split('.')
        except ValueError:
            raise BadModelFormatError(model)
        model_cls = get_model(app_name, model_name)
        if not model_cls:
            raise ModelImportError(app_name, model_name)

        # Add some attributes to the wrapped method for use by
        # FactoryMetaclass.
        _wrapped_func._factories_model = model_cls
        _wrapped_func._factories_blueprint = True
        _wrapped_func.__doc__ = 'Blueprint: ' + _wrapped_func.__doc__

        return _wrapped_func
    return _decorator


class ModelImportError(Exception):
    "Unable to import model from string."
    def __init__(self, app_name, model_name):
        self.app_name = app_name
        self.model_name = model_name

    def __str__(self):
        return "Could not import model '%s': Perhaps '%s' is not in your INSTALLED_APPS or there is a typo?" % (self.model_name, self.app_name)


class BadModelFormatError(Exception):
    "Model argument to blueprint decorator was malformed."
    def __init__(self, model_str):
        self.model_str = model_str

    def __str__(self):
        return "Value for model argument to blueprint decorator is malformed ('%s').  Expected format is 'app_name.ModelName'." % self.model_str
