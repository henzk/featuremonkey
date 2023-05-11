"""
private helpers
"""

import inspect
import sys

from functools import wraps


def _delegate(to):
    @wraps(to)
    def original_wrapper(throwaway, *args, **kws):
        return to(*args, **kws)

    return original_wrapper


def _is_class_instance(obj):
    return not inspect.isclass(obj) and not inspect.ismodule(obj)


def _get_role_name(role):
    if inspect.ismodule(role):
        return role.__name__
    return role.__class__.__name__


def _get_base_name(base):
    name = getattr(base, '__name__', repr(base))
    return "%s:%s" % (name, base.__class__.__name__)


def _get_method(method, base):
    if _is_class_instance(base):
        return method.__get__(base, base.__class__)
    else:
        return method


if sys.version_info < (2, 7):

    def _extract_staticmethod(m):
        return m.__get__(True)

    def _extract_classmethod(m):
        return m.__get__(True).im_func

else:

    def _extract_staticmethod(m):
        return m.__func__

    _extract_classmethod = _extract_staticmethod
