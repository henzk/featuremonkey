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
However, large components are often very specific which limits their reuse;
many small components often make it necessary to write a large amount of glue code to integrate them.

So components are nice --- but it feels like there is something missing.

Features provide an additional dimension of modularity by allowing the developer to encapsulate
code related to a specific concern that is scattered across multiple locations of the codebase into so-called *feature modules*.
Products can then be composed automatically by selecting a set of these feature modules.

Common approaches to FOSD are the use of generative techniques 
i.e. statically composing a product`s code and other artefacts 
as part of the build process e.g. `FeatureHouse <http://fosd.net/fh>`_,
the use of specialized programming languages with feature support e.g. `FeatureC++ <http://fosd.net/fcc>`_,
or by making features explicit using IDE support e.g. `CIDE <http://fosd.net/cide>`_.

``featuremonkey`` implements feature composition by using monkeypatching i.e. structures are dynamically modified at runtime.


*******************************************
Fun facts on featuremonkey for FOSD people
*******************************************

- dynamic feature binding at startup time or later
- no unbind
- in Python everything is an object --- ``featuremonkey`` composes objects
- function/method refinements are implemented as delegation layers(wrappers wrapping wrappers wrapping ...)
- uses monkeypatching to bind features --- dynamic program modification

The central operation exposed by ``featuremonkey`` is ``compose``.
It applies transformations.

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

