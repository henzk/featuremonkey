from __future__ import absolute_import
from featuremonkey.composer import Composer

__version__ = '0.2.1'
__author__ = 'Hendrik Speidel <hendrik@schnapptack.de>'
#setup default composer and provide access to its methods at the module level
_default_composer = Composer()
select = _default_composer.select
select_equation = _default_composer.select_equation
compose = _default_composer.compose
compose_later = _default_composer.compose_later
