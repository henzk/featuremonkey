"""
Serialization module
====================



"""
import collections
import inspect

import marshal

from .helper import (
    is_class_method,
    is_static_method
)


def _serialize_method(obj):
    return _serialize_function(obj)


def _serialize_function(obj):
    """
    Still needing this much try-except stuff. We should find a way to get rid of this.
    :param obj:
    :return:
    """
    try:
        obj = inspect.getsource(obj)
    except (TypeError, IOError):
        try:
            obj = marshal.dumps(obj)
        except ValueError:
            if hasattr(obj, '__dict__'):
                obj = _serialize_dict(obj.__dict__)
    return obj


def _serialize_module(obj):
    return obj


def _serialize_class(obj):
    if hasattr(obj, '__dict__'):
        obj = _serialize_dict(obj.__dict__)
    return obj


def _serialize_classmethod(obj):
    return _serialize_function(obj)


def _serialize_staticmethod(obj):
    return _serialize_function(obj)


def _serialize_callable(obj):
    if inspect.isclass(obj):
        obj = _serialize_class(obj)
    elif inspect.ismethod(obj) and is_class_method(obj):
        obj = _serialize_classmethod(obj)
    elif inspect.ismethod(obj) and is_static_method(obj):
        obj = _serialize_staticmethod(obj)
    elif inspect.ismethod(obj):
        obj = _serialize_method(obj)
    elif inspect.isfunction(obj):
        obj = _serialize_function(obj)
    return obj


def _serialize_iterable(obj):
    """
    Only for serializing list and tuples and stuff.
    Dicts and Strings/Unicode is treated differently.
    String/Unicode normally don't need further serialization and it would cause
    a max recursion error trying to do so.
    :param obj:
    :return:
    """
    for item in obj:
        obj[obj.index(item)] = serialize_obj(item)
    return obj


def _serialize_dict(obj):
    for k, v in obj.items():
        obj[k] = serialize_obj(v)
    return obj


def serialize_obj(obj):
    if callable(obj):
        obj = _serialize_callable(obj)
    elif inspect.ismodule(obj):
        obj = _serialize_module(obj)
    elif isinstance(obj, collections.Iterable) and not isinstance(obj, (str, dict, unicode)):
        obj = _serialize_iterable(obj)
    elif isinstance(obj, dict):
        obj = _serialize_dict(obj)
    elif hasattr(obj, '__dict__'):
        obj = _serialize_dict(obj.__dict__)
    elif not isinstance(obj, (str, unicode)):
        obj = repr(obj)
    return obj


def serialize_operation_log(operation_log):
    for operation in operation_log:
        operation['old_value'] = serialize_obj(operation['old_value'])
        operation['new_value'] = serialize_obj(operation['new_value'])
    return operation_log
