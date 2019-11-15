
'''
References:
-----------

Liu, Feilong. "An efficient centroid type-reduction 
strategy for general type-2 fuzzy logic system." 
Information Sciences 178.9 (2008): 2224-2236.
'''
import numpy as np
import math
import os
from type2fuzzy.membership.type1fuzzyset import Type1FuzzySet
from type2fuzzy.membership.generaltype2fuzzyset import GeneralType2FuzzySet
from type2fuzzy.membership.intervaltype2fuzzyset import IntervalType2FuzzySet
from type2fuzzy.display.setplotter import SetPlotter
from type2fuzzy.membership.zslicetype2fuzzyset import ZSliceType2FuzzySet
from type2fuzzy.type_reduction.it2_karnikmendel_reducer import it2_kernikmendel_reduce

from type2fuzzy import zslice_hagras_reduce
from type2fuzzy import IntervalType2FuzzySet

def adjust_value(val, val_array):
	idx = (np.abs(val_array - val)).argmin()
	return val_array[idx]
 
def generate_set(w=1):

	gt2fs = GeneralType2FuzzySet()
	x_resolution = 1001
	y_resolution = 601

	y =  np.linspace(0, 1, y_resolution)
	primary_domain = np.linspace(0, 10, x_resolution)

	for x in primary_domain:
		upper_mf_val =  adjust_value(max(1.0 * math.exp(-math.pow(x-3, 2)/8), 0.8 * math.exp(-math.pow(x-6, 2)/8)), y)

		mid_mf_val =    adjust_value(max(0.75 * math.exp(-math.pow(x-3, 2)/5), 0.6 * math.exp(-math.pow(x-6, 2)/5)), y)

		lower_mf_val =  adjust_value(max(0.5 * math.exp(-math.pow(x-3, 2)/2), 0.4 * math.exp(-math.pow(x-6, 2)/2)), y)

		# mid_pt =  adjust_value(((upper_mf_val + lower_mf_val) / 2), y)

		mf = Type1FuzzySet.create_triangular_ex(y, lower_mf_val, mid_mf_val, upper_mf_val)
		gt2fs.add_membership_function(x, mf)

	return gt2fs

plotter = SetPlotter()	
gt2fs = generate_set()
slice_4 = gt2fs[4]


zt2fs = ZSliceType2FuzzySet.from_general_type2_set(gt2fs, 100)
centroid = zslice_hagras_reduce(zt2fs)

print(centroid)
centroid_t1 = Type1FuzzySet.from_alphacut_type1_set(centroid)

it2fs = gt2fs.z_slice(1.0)


plotter.add_generaltype2set(gt2fs)
plotter.add_generaltype2set(gt2fs)
plotter.add_generaltype2set(gt2fs)
plotter.add_generaltype2set(gt2fs)
# plotter.add_type1fuzzyset(slice)
# plotter.add_invervaltype2set(it2fs)
# plotter.add_type1fuzzyset(centroid_t1)



plotter.plot(2)