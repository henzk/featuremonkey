
***************************************
Changelog
***************************************

**HEAD**

**0.3.0**

- better error messages
- feature.py is now mandatory for features
- compose_later also accepts transformations specified as strings (these are assumed to be module names and will be imported at composition time)
- function refinements that don't carry docstrings now use the docstring of their original

**0.2.2**

- added ``get_features_from_equation_file`` to public API
- added import guards
- split into multiple files
- **backwards incompatible change:** signatures of ``feature.select`` functions need to be changed from ``feature.select`` to ``feature.select(composer)``.

**0.2.1**

- more docs
- raises ``CompositionError`` consistently

**0.2**


- first release on PYPI
- composer is now class based
- fixes compose_later composition order
- initial docs

**0.1**

- initial version

