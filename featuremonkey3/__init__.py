from __future__ import absolute_import
from featuremonkey3.composer import (Composer,
    get_features_from_equation_file,
    CompositionError)

from featuremonkey3.importhooks import ImportGuardHook

__version__ = '0.3.1'
__author__ = 'Hendrik Speidel <hendrik@schnapptack.de>'


add_import_guard = ImportGuardHook.add
remove_import_guard = ImportGuardHook.remove

# setup default composer and provide access to its methods at the module level
_default_composer = Composer()
select = _default_composer.select
select_equation = _default_composer.select_equation
compose = _default_composer.compose
compose_later = _default_composer.compose_later
