'''
composer.py - feature oriented composition of python code
'''
from __future__ import absolute_import
import inspect
import importlib
import sys
from functools import wraps
from .importhooks import LazyComposerHook
from .helpers import (_delegate, _is_class_instance, _get_role_name,
    _get_base_name, _get_method)

def get_features_from_equation_file(filename):
    '''
    returns list of feature names read from equation file given
    by ``filename``.

    format: one feature per line; comments start with ``#``

    Example::

        #this is a comment
        basefeature
        #empty lines are ignored

        myfeature
        anotherfeature

    '''
    features = []
    for line in open(filename):
        line = line.split('#')[0].strip()
        if line:
            features.append(line)
    return features

class CompositionError(Exception): pass

class Composer(object):


    def _introduce(self, role, target_attrname, attr, base):
        if hasattr(base, target_attrname):
            raise CompositionError(
                'Cannot introduce "%s" from "%s" into "%s"!'
                ' Attribute exists already!' % (
                    target_attrname,
                    _get_role_name(role),
                    _get_base_name(base),
                )
            )
        if callable(attr):
            evaluated_attr = attr()
            if not callable(evaluated_attr):
                raise CompositionError(
                    'Cannot introduce "%s" from "%s" into "%s"!'
                    ' Method Introduction is not callable!' % (
                        target_attrname,
                        _get_role_name(role),
                        _get_base_name(base),
                    )
                )
            setattr(base, target_attrname, _get_method(evaluated_attr, base))
        else:
            setattr(base, target_attrname, attr)


    def _refine(self, role, target_attrname, attr, base):
        if not hasattr(base, target_attrname):
            raise CompositionError(
                'Cannot refine "%s" of "%s" by "%s"!'
                ' Attribute does not exist in original!' % (
                    target_attrname,
                    _get_base_name(base),
                    _get_role_name(role),
                )
            )
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


    def _apply_operation(self, role, base, attr, attrname):
        if attrname.startswith('introduce_'):
            target_attrname = attrname[len('introduce_'):]
            self._introduce(role, target_attrname, attr, base)
        elif attrname.startswith('refine_'):
            target_attrname = attrname[len('refine_'):]
            self._refine(role, target_attrname, attr, base)
        elif attrname.startswith('child_'):
            target_attrname = attrname[len('child_'):]
            refinement = attr()
            self.compose(refinement, getattr(base, target_attrname))

    def _compose_pair(self, role, base):
        '''
        composes onto base by applying the role
        '''
        for attrname in dir(role):
            attr = getattr(role, attrname)
            self._apply_operation(role, base, attr, attrname)

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
            raise CompositionError('nothing to compose')
        if len(things) == 1:
            #composing one element is simple
            return things[0]
        else:
            #recurse after applying last role to object
            return self.compose(*(
                list(things[:-2]) #all but the last two 
                #plus the composition of the last two
                + [self._compose_pair(things[-2], things[-1])]
            ))


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
            raise CompositionError(
                'compose_later call after module has been imported: '
                 + module_name
            )
        LazyComposerHook.add(module_name, things[:-1], self)


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
                if not hasattr(feature_spec_module, 'select'):
                    raise CompositionError(
                        'Function %s.feature.select not found!\n '
                        'Feature modules need to specify a function'
                        ' select(composer).' % (
                            feature_name
                        )
                    )
                args, varargs, keywords, defaults = inspect.getargspec(
                    feature_spec_module.select
                )
                if varargs or keywords or defaults or len(args) != 1:
                    raise CompositionError(
                        'invalid signature: %s.feature.select must '
                        'have the signature select(composer)' % (
                            feature_name
                        )
                    )
                #call the feature`s select function
                feature_spec_module.select(self)
            except ImportError:
                pass


    def select_equation(self, filename):
        """
        select features from equation file

        format: one feature per line; comments start with ``#``

        Example::

            #this is a comment
            basefeature
            #empty lines are ignored

            myfeature
            anotherfeature

        """
        features = get_features_from_equation_file(filename)
        self.select(*features)
