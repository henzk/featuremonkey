##########################################
Welcome to featuremonkey's documentation!
##########################################

    ``featuremonkey`` is a tool to support *feature oriented programming (FOP)* in python.


``featuremonkey`` is a tiny library to enable feature oriented programming (FOP) in Python.
Feature oriented software development(FOSD) is a methodology to build and maintain software product lines.
Products are composed automatically from a set of feature modules and may share a set of features and differ in others.

There are multiple definitions of what a feature really is. Here, we use the definition of Apel et al.:

    A feature is a structure that extends and modifies the structure of
    a given program in order to satisfy a stakeholder’s requirement,
    to implement and encapsulate a design decision,
    and to offer a configuration option [ALMK]_ .

When trying to modularize software-systems to acheive reusability, components come to mind.
However, there is a problem with that: large components are very specific which limits reuse;
many small components often make it necessary to write larger amounts of glue code to integrate them.

So components are nice --- but it feels like there is something missing.

Features provide an additional dimension of modularity by allowing the developer to encapsulate
code related to a specific concern that is scattered across multiple locations of the codebase into feature modules.
Products can then be composed automatically by selecting a set of feature modules.

Common approaches to FOSD are the use of generative techniques 
i.e. composing a product`s code and other artefacts as part of the build process,
the use of specialized programming languages with feature support,
or making features explicit using IDE support.

``featuremonkey`` implements feature composition by using monkeypatching i.e. structures are dynamically redefined at runtime.


*******************************************
Fun facts on featuremonkey for FOSD people
*******************************************


- features are bound at startup time or later (dynamic feature binding)
- however, feature binding is not fully dynamic as there is no way to unbind a feature once it has been bound.
- featuremonkey uses delegation layers that are injected at runtime when composing the features.
- featuremonkey composes objects(instances that is)
- packages, modules, classes, functions, methods and so on are all objects in python ... therefore, featuremonkey can compose those as well.
- featuremonkey uses monkeypatching to bind features: it adapts the interpreter state.


The basic operation  offered by ``featuremonkey`` is ``compose``.

***************************************
Feature Oriented Software Development
***************************************

.. toctree::
    :maxdepth: 2
    
    fosd

***************************************
Getting started
***************************************

.. toctree::
    :maxdepth: 2
    
    install
    tutorial

***************************************
featuremonkey Reference
***************************************

.. toctree::
    :maxdepth: 2
    
    reference


*********************
Indices and tables
*********************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


**********************
Changelog
**********************

.. toctree::
    :maxdepth: 2

    changelog


.. [ALMK] S. Apel, C. Lengauer, B. Möller, and C. Kästner.
    An Algebra for Features and Feature Composition.
    In Proceedings of the International Conference on 
    Algebraic Methodology and Software Technology (AMAST),
    volume 5140 of Lecture Notes in Computer Science,
    pages 36–50. Springer-Verlag, 2008.

