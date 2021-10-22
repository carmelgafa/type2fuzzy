import numpy as np
import itertools
from type2fuzzy.membership.type1fuzzyset import Type1FuzzySet


def gt2_mendeljohn_reduce(gt2fs, precision=5, information='none'):
	'''
	References:
	-----------
	Karnik, Nilesh N., and Jerry M. Mendel. "Centroid of a type-2 fuzzy set." 
	Information Sciences 132.1-4 (2001): 195-220.

	Arguments:
	----------
	gt2fs -- the general type 2 fuzzy set
	precision -- the precision applied when computing N/D and F
	information -- the amount of information given to the user;
		none - no information
	'''

	reduced_set = None

	if information == 'none':
		reduced_set = _gt2_mendeljohn_noinfo(gt2fs, precision)
	
	return reduced_set

def _gt2_mendeljohn_noinfo(gt2fs, precision=5):
	'''
	References:
	-----------
	Karnik, Nilesh N., and Jerry M. Mendel. "Centroid of a type-2 fuzzy set." 
	Information Sciences 132.1-4 (2001): 195-220.
	'''
	set_array = []
	primary_domain, secondary_domain, set_array = gt2fs.to_array_explicit()

	# get an index array
	index_array = np.indices(set_array.shape)[0]

	# create a list with the number of non zero elements in each vertical slice
	# i.e. the number of non xero element in each column
	col_gen = [index_array[set_array[:, x] > 0, x] for x in range(set_array.shape[1])]

	# the number of columns is the number of elements in the domain
	domain_index = range(0, set_array.shape[1])

	reduced_set = Type1FuzzySet()
	# for every comination of the column elemnets create a type 2 embedded fuzzy set
	for t in itertools.product(*col_gen):
		embedded = list(map(lambda i: (set_array[t[i]][i], secondary_domain[t[i]], primary_domain[i]) , domain_index))
		dom = 1
		cog_numerator = 0
		cog_denominator = 0
		for point in embedded:
			dom = min(dom, point[0])
			cog_numerator = cog_numerator +(point[1] * point[2])
			cog_denominator = cog_denominator +(point[1])

		if cog_denominator > 0:
			reduced_set.add_element(round(cog_numerator/cog_denominator, precision), dom)
			
	return reduced_set
