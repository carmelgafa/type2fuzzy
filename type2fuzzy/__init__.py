"""
Recommended Use
---------------
>>> import type2fuzzy as t2f
"""
__all__ = []

import type2fuzzy.membership as _membership
import type2fuzzy.display as _display
import type2fuzzy.type_reduction as _tr
import type2fuzzy.type1_defuzzification as _t1defuzz
import type2fuzzy.measurement as _measure

from type2fuzzy.membership import *
from type2fuzzy.display import *
from type2fuzzy.type_reduction import *
from type2fuzzy.type1_defuzzification import *
from type2fuzzy.measurement import *

__all__.extend(_membership.__all__)
__all__.extend(_display.__all__)
__all__.extend(_tr.__all__)
__all__.extend(_t1defuzz.__all__)
__all__.extend(_measure.__all__)


__author__  = 'Carmel Gafa'
__email__ = 'carmelgafa@gmail.com'
__copyright__ = '"Copyright 2007, Carmel Gafa"'
__status__  = "alpha"
__version__ = "0.1"
__date__    = "01 April 2019"