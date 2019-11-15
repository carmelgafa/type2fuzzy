import logging
from type2fuzzy.membership.zslicetype2fuzzyset import ZSliceType2FuzzySet
from type2fuzzy.membership.alphacuttype1fuzzyset import AlphaCutType1FuzzySet
from type2fuzzy.type_reduction.it2_karnikmendel_reducer import it2_kernikmendel_reduce

def zslice_hagras_reduce(zt2fs, precision=5, information='none'):
	'''
	References:
	-----------


	Arguments:
	----------
	zt2fs -- the z-slice type 2 fuzzy set
	precision -- the precision applied when computing N/D and F
	information -- the amount of information given to the user;
		none - no information
	'''

	reduced_set = None

	if information == 'none':
		reduced_set = _zslice_hagras_noinfo(zt2fs, precision)
	elif information == 'full':
		reduced_set = _zslice_hagras_fullinfo(zt2fs, precision)
	
	return reduced_set

def _zslice_hagras_noinfo(zt2fs, precision):
	'''
	Type reduction for z-slice type-2 fuzzy set using Hagras algorithm
	logging no the information during the execution.
	'''

	reduced_set = AlphaCutType1FuzzySet()

	zslices = zt2fs.zslices()


	for zslice in zslices:

		it2fs = zt2fs[zslice]

		centroid = it2_kernikmendel_reduce(it2fs, precision=precision)

		reduced_set.add_element(zslice, centroid)

	return reduced_set


def _zslice_hagras_fullinfo(zt2fs, precision):
	'''
	Type reduction for z-slice type-2 fuzzy set using Hagras algorithm
	logging all the information during the execution.
	'''

	reduced_set = AlphaCutType1FuzzySet()

	for zslice in zt2fs.zslices():
		logging.log(logging.DEBUG, f'z-slice value: {zslice}')
		
		it2fs = zt2fs[zslice]
		logging.log(logging.DEBUG, f'correspnding set:{it2fs}')

		if not it2fs.empty:
			centroid = it2_kernikmendel_reduce(it2fs, precision=precision)
			logging.log(logging.DEBUG, f'centroid of interval set:{centroid}')
			if not centroid.empty:
				reduced_set.add_element(zslice, centroid)

	logging.log(logging.DEBUG, f'reduced set: {reduced_set}')

	return reduced_set