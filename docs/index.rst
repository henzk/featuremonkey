##########################################
Welcome to featuremonkey's documentation!
##########################################

    featuremonkey is a tool to ease *feature oriented programming (FOP)* in python.


featuremonkey is a tiny library to enable FOP(feature oriented programming) in Python.
Feature composition is realized using monkeypatching i.e. structures are dynamically redefined at runtime.
This way featuremonkey gives you nice stacktraces if something should go wrong - it propably will.
However, this dynamic approach is not without its drawbacks: first, it creates some overhead at runtime and second due to the dynamic nature and the non-existant type-system some error classes that are detected before running the program with featurehouse emerge at runtime later.

``featuremonkey`` uses the concept of FST superimposition to compose products out of a list of features.
In contrast to other feature oriented composition approaches like ``featureHouse``, ``featuremonkey`` operates at runtime.

Now, suppose we wanted to add functionality to that program without touching it.
Therefore, we write the additions and modifications to the base program 
in form of an FST.

The documentation begins with some background information
and then dives into feature oriented python programming using featuremonkey.

*******************************************
Fun facts on featuremonkey for FOSD people
*******************************************


- features are bound at startup time or later (dynamic feature binding)
- however, feature binding is not fully dynamic as there is no way to unbind a feature once it has been bound.
- featuremonkey uses delegation layers that are injected at runtime to compose the features.
- featuremonkey composes objects(instances that is)
- packages, modules, classes, functions, methods and so on are all objects in python ... therefore, featuremonkey can compose those as well.
- featuremonkey uses monkeypatching to bind features: it adapts the interpreter state.



The basic featuremonkey operation is ``compose``. It superimposes FST modules/classes onto the current interpreter state.

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

