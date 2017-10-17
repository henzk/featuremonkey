# coding: utf-8
from __future__ import unicode_literals

import inspect


def is_static_method(obj):
    klass = get_class_from_method(obj)
    if not klass:
        return False
    for cls in inspect.getmro(klass):
        if inspect.isroutine(obj):
            binded_value = cls.__dict__.get(obj.__name__)
            if isinstance(binded_value, staticmethod):
                return True


def get_class_from_method(obj):
    for cls in inspect.getmro(obj.im_class):
        if obj.__name__ in cls.__dict__:
            return cls


def is_class_method(obj):
    klass = get_class_from_method(obj)
    if not klass:
        return False
    return hasattr(klass, '__dict__') and isinstance(klass.__dict__.get(obj.__name__), classmethod)
