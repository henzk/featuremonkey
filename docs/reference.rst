************************
featuremonkey Reference
************************

Feature Composition
=======================

A feature bundles *introductions* and *refinements* to the codebase.
Introductions are additions to the codebase, refinements allow certain modifications of existing code.

We will use *structure transformation* or transformation as the more generic term, when referring to introductions and refinements
(Often, refinement is used instead, because technically an introduction is a form of refinement --- transformation is used here just to avoid confusion).

The process of actually applying the introductions and modifications of a given feature is called *feature binding*.

*Feature Composition* is the stepwise binding of a *feature selection* --- a specified set of features in a specified order.


Feature Layout
===================

Features are represented as Python packages.
The feature name is defined as the fully qualified name of the package.

The package needs to define a module called ``feature``,
which must define a function ``select(composer)``.

This function is called by the composer to bind the feature.
Its purpose is to apply the structure transformations defined by the feature
using the composer, which gets passed in as sole argument.


File Structure
-------------------

::

    myfeature/
        __init__.py
        feature.py


Above, mandatory files to specify a feature called ``myfeature`` are listed.
Additionally, features may contain other modules, subpackages and also non-Python files.

Note: ``__init__.py`` is needed to mark the directory as a python package.


::

    #myfeature/feature.py

    def select(composer):
        #bind myfeature by applying necessary transformations

        #apply transformation myfeature.mymodule to basefeature.mymodule
        from . import mymodule
        import basefeature.mymodule
        composer.compose(mymodule, basefeature.mymodule)


Here, the example of a ``feature`` module inside a feature package is given.

``select`` is mandatory, but may be empty if there are no transformations to apply, e.g. in case of the base feature.

In the following, the different types of structure transformations offered by the composer
are described.


Feature Structure Trees
=========================

featuremonkey recognizes python packages, modules, classes, functions and methods as being part of the FST.


FST Declaration
=================

FSTs are declared as modules or classes depending on the preference of the user. modules and classes can be mixed arbitrarily.

.. note::

    when using classes, please make sure to use new style classes. Old style classes are completely unsupported by featuremonkey - because they are old and are removed from the python language with 3.0. To create a new style class, simply inherit from ``object`` or another new style class explicitely.

FSTs specify introductions and refinements of structures contained in the global interpreter state.
This is done by defining specially crafted names inside the FST module/class.

FST Introduction
-------------------

Introductions are useful to add new attributes to existing packages/modules/classes/instances.

An introduction is specified by creating a name starting with ``introduce_`` followed by the name to introduce directly inside the FST module/class.
The attribute value will be used like so to derive the value to introduce:

- If the FST attribute value is not callable, it is used as the value to introduce without further processing.
- If it is a callable, it is called to obtain the value to introduce. The callable will be called without arguments and must return this value.

Example::

    class TestFST1(object):
        #introduce name ``a`` with value ``7``
        introduce_a = 7

        #introduce name ``b`` with value ``6``
        def introduce_b(self):
            return 6

        #introduce method ``foo`` that returns ``42`` when called
        def introduce_foo(self): 
            def foo(self):
                return 42
            
            return foo


.. warning::

    Names can only be introduced if they do not already exist in the current interpreter state.
    Otherwise ``compose`` will raise a ``CompositionError``. If that happens, the product may be in an
    inconsistent state. Consider restarting the whole product!
    

FST Refinement
-------------------


Refinements are used to refine existing attributes of packages/modules/classes/instances.

An introduction is specified much like an introduction.
It is done by creating a name starting with ``refine_`` followed by the name to refine directly inside the FST module/class.
The attribute value will be used like so to derive the value to introduce:

- If the FST attribute value is not callable, it is used as the refined value without further processing. **This is a replacement**
- If it is a callable e.g. a method, it is called to obtain the refined value. The callable will be called with the single argument ``original`` and must return this value. ``original`` is a reference to the current implementation of the name that is to be refined. It is analogous to ``super`` in OOP.

Example::

    class TestFST1(object):
        #refine name ``a`` with value ``7``
        refine_a = 7

        #refine name ``b`` with value ``6``
        def introduce_b(self, original):
            return 6

        #refine method ``foo`` to make it return double the value of before.
        def refine_foo(self, original): 
            def foo(self):
                return orginal(self) * 2
            
            return foo


.. note::

    when calling ``original`` in a method refinement(for both classes and instances), you need to explicitely pass ``self`` as first parameter to ``original``.


.. warning::

    Names can only be refined if they exist in the current interpreter state.
    Otherwise ``compose`` will raise a ``CompositionError``. If that happens, the product may be in an
    inconsistent state. Consider restarting the whole product!


FST nesting
===================

FSTs can be nested to refine nested structures of the interpreter state.
To create a child FST node, create a name starting with ``child_`` followed by the nested name.
The value must be either a FST class or instance or a FST module.
As an example, consider a refinement to the ``os`` module.
We want to introduce ``os.foo`` and also refine ``os.path.join``.
We could do this by composing a FST on ``os`` to introduce ``foo`` and then composing another FST on ``os.path`` that refines ``join``.
Alternatively, we can use FST nesting and specify it as follows::

    class os(object):
        introduce_foo = 123
        class child_path(object):
            def refine_join(self, original):
                def join(*elems):
                    return original(elems)
                return join


Got it?


FST Composition
===================

.. autofunction:: featuremonkey.compose


.. autofunction:: featuremonkey.compose_later






Product Selection
===================

.. autofunction:: featuremonkey.select

.. autofunction:: featuremonkey.select_equation


Import Guards
=================

.. autoclass:: featuremonkey.importhooks.ImportGuardHook

.. autofunction:: featuremonkey.add_import_guard(module_name, msg='')

.. autofunction:: featuremonkey.remove_import_guard(module_name)


Example::

    >>> import featuremonkey
    >>> featuremonkey.add_import_guard('django')
    >>> import django
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "featuremonkey/importhooks.py", line 160, in load_module
        + (self._guards[module_name][-1] or module_name)
    featuremonkey.importhooks.ImportGuard: Import while import guard in place: django
    >>> featuremonkey.remove_import_guard('django')
    >>> import django
    >>> 


First an import guard is created for the package ``django``.
Then, we try to import it and an ``ImportGuard`` is raised.
After we remove the guard again, we can import the package without an error.

Utilities
===============

.. autofunction:: featuremonkey.get_features_from_equation_file
