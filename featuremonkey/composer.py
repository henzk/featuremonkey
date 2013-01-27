'''
composer.py - feature oriented composition of python code
'''
from __future__ import absolute_import
import inspect
import importlib
import sys


def _delegate(to):

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
    return "%s:%s" % (base.__name__, base.__class__.__name__)


def _get_method(method, base):
    if _is_class_instance(base):
        return method.__get__(base, base.__class__)
    else:
        return method

class LazyComposer(object):
    _to_compose = dict()


    @classmethod
    def add(cls, module_name, fsts):
        if not module_name in cls._to_compose:
            cls._to_compose[module_name] = []
        cls._to_compose[module_name] += fsts


    def find_module(self, fullname, path=None):
        if fullname in self._to_compose:
            return self


    def load_module(self, module_name):
        fsts = self._to_compose.pop(module_name)
        module = importlib.import_module(module_name)
        fsts.reverse()
        fsts.append(module)
        compose(*fsts)
        return module


#register import hook
sys.meta_path.append(LazyComposer())

class Composer(object):


    def _introduce(self, role, attrname, attr, base):
        target_attrname = attrname[len('introduce_'):]
        if hasattr(base, target_attrname):
            raise Exception('Cannot introduce "%s" from "%s" into "%s"! Attribute exists already!' % (
                target_attrname,
                _get_role_name(role),
                _get_base_name(base),
            ))
        if callable(attr):
            evaluated_attr = attr()
            if not callable(evaluated_attr):
                raise Exception('Cannot introduce "%s" from "%s" into "%s"! Method Introduction is not callable!' % (
                    target_attrname,
                    _get_role_name(role),
                    _get_base_name(base),
                ))
            setattr(base, target_attrname, _get_method(evaluated_attr, base))
        else:
            setattr(base, target_attrname, attr)


    def _refine(self, role, attrname, attr, base):
        target_attrname = attrname[len('refine_'):]
        if not hasattr(base, target_attrname):
            raise Exception('Cannot refine "%s" of "%s" by "%s"! Attribute does not exist in original!' % (
                target_attrname,
                _get_base_name(base),
                _get_role_name(role),
            ))
        if callable(attr):
            baseattr = getattr(base, target_attrname)
            if callable(baseattr):
                if inspect.isclass(base) or inspect.ismodule(base):
                    setattr(base, target_attrname, _get_method(attr(baseattr), base))
                else:
                    setattr(base, target_attrname, _get_method(attr(_delegate(baseattr)), base))
            else:
                setattr(base, target_attrname, attr(baseattr))
        else:
            setattr(base, target_attrname, attr)


    def _compose_pair(self, role, base):
        '''
        composes onto base by applying the role
        '''
        for attrname in dir(role):
            attr = getattr(role, attrname)
            if attrname.startswith('introduce_'):
                self._introduce(role, attrname, attr, base)
            elif attrname.startswith('refine_'):
                self._refine(role, attrname, attr, base)
            elif attrname.startswith('child_'):
                target_attrname = attrname[len('child_'):]
                refinement = attr()
                self.compose(refinement, getattr(base, target_attrname))
        return base


    def compose(self, *things):
        '''
        compose applies multiple fsts onto a base implementation.
        Pass the base implementation as last parameter.
        fsts are merged from RIGHT TO LEFT (like function application)
        e.g.:

        class MyFST(object):
            #place introductions and refinements here
            introduce_foo = 'bar'

        compose(MyFST(), MyClass)
        '''
        if not len(things):
            raise Exception('nothing to compose')
        if len(things) == 1:
            return things[0]
        else:
            #recurse after applying last role to object
            return compose(*(list(things[:-2]) + [self._compose_pair(things[-2], things[-1])]))


    def compose_later(self, *things):
        """
        register list of things for composition using compose()

        compose_later takes a list of fsts.
        The last element specifies the base module as string
        things are composed directly after the base module
        is imported by application code
        """
        if len(things) == 1:
            return things[0]
        module_name = things[-1]
        if module_name in sys.modules:
            raise Exception('compose_later call after module has been imported: ' + module_name)
        LazyComposer.add(module_name, things[:-1])


    def select(self, *features):
        """
        selects the features given as string
        e.g
        passing 'hello' and 'world' will result in imports of
        'hello' and 'world'. Then, if possible 'hello.feature'
        and 'world.feature' are imported and select is called
        in each feature module.
        """
        for feature_name in features:
            feature_module = importlib.import_module(feature_name)
            #if available, import feature.py and select the feature
            try:
                feature_spec_module = importlib.import_module(
                    feature_name + '.feature'
                )
                feature_spec_module.select()
            except ImportError:
                pass


    def select_equation(self, filename):
        features = []
        for line in open(filename):
            line = line.strip()
            if line and not line.startswith('#'):
                features.append(line)
        self.select(*features)


_default_composer = Composer()
select = _default_composer.select
select_equation = _default_composer.select_equation
compose = _default_composer.compose
compose_later = _default_composer.compose_later
