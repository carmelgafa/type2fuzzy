"""
type2fuzzy.type1_defuzzification : type-1 defuzzification methods
"""
from type2fuzzy.type1_defuzzification.cog_defuzzifier import cog_defuzzify
from type2fuzzy.type1_defuzzification.mom_defuzzifier import mom_defuzzify
from type2fuzzy.type1_defuzzification.zslice_centroid_defuzzifier import zslice_centroid_defuzzify

__all__ = ['cog_defuzzify', 'mom_defuzzify', 'zslice_centroid_defuzzify']
