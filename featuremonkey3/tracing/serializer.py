# coding: utf-8
from __future__ import unicode_literals

"""
Serialization module
====================

Serializes the data of the Composers operation log which can then be
used for further processing and analysis (e.g. collaboration diagrams).

serialize_obj can still be used for any kind of serialization of python objects.

The following objects can be composed by featuremonkey:
    - functions
    - classmethods
    - staticmethods
    - methods
    - classes
    - modules
    - simple objects (str, int, ...)
    - iterables (str, lists, tuples, sets, dicts, ...)
    - etc...

For all these types of objects there are new serialization methods required which are not
completely provided by the packages of the python standard library.
Therefore, custom serialization is required:
    - for functions and methods the actual source code is required
    - serialization of functions can be tricky in case they have a decorator (e.g. ape tasks).
      In this case they are wrapped, therefore, the content of the function must be obtained from the wrapper.
    - for simple objects and iterables (in case the iterables contain simple objects) simply their values
    - for classes, in most cases their __dict__ representation is enough
    - for modules maybe also recursively serialize its __dict__ ? -> tbd
"""

import collections
import inspect
import marshal
import six

from io import IOBase

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
    """
    Tries to serialize a module by its __dict__ attr.
    Remove the builtins attr as this one is not relevant and extremely large.
    If its value is a callable, serialize it using serialize_obj, else, use its repr,
    because in this case we most likely run into max recursion depth errors.
    :param obj:
    :return:
    """
    obj = dict(obj.__dict__)
    if '__builtins__' in obj.keys():
        obj.pop('__builtins__')
    for k, v in obj.items():
        if callable(v):
            obj[k] = serialize_obj(v)
        else:
            obj[k] = repr(v)
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
    if isinstance(obj, (tuple, set)):
        # make a tuple assignable by casting it to list
        obj = list(obj)
    for item in obj:
        obj[obj.index(item)] = serialize_obj(item)
    return obj


def _serialize_dict(obj):
    obj = dict(obj)
    for k, v in obj.items():
        obj[k] = serialize_obj(v)
    return obj


def serialize_obj(obj):
    if callable(obj):
        obj = _serialize_callable(obj)
    elif inspect.ismodule(obj):
        obj = _serialize_module(obj)
    elif isinstance(obj, collections.Iterable) and not isinstance(obj, (str, dict, six.text_type, IOBase)):
        # "six.text_type" is "unicode" in py2 and "str" in py3
        # "IOBase" is the same check as for "file" in py2, but compatible for both
        obj = _serialize_iterable(obj)
    elif isinstance(obj, dict):
        obj = _serialize_dict(obj)
    elif hasattr(obj, '__dict__'):
        obj = _serialize_dict(obj.__dict__)
    elif not isinstance(obj, (str, six.text_type)):
        obj = repr(obj)
    return obj


def serialize_operation_log(operation_log):
    for operation in operation_log:
        operation['old_value'] = serialize_obj(operation['old_value'])
        operation['new_value'] = serialize_obj(operation['new_value'])
    return operation_log
