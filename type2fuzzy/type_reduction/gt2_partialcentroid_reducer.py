from type2fuzzy.membership.generaltype2fuzzyset import GeneralType2FuzzySet
from type2fuzzy.membership.type1fuzzyset import Type1FuzzySet

def gt2_partialcentroid_reduce(gt2fs, precision=5, information='none'):
	'''
	References:
	-----------
	Gafa, Carmel, and Simon Coupland. 
	"A new recursive type-reduction procedure for general type-2 fuzzy sets."
	Advances in Type-2 Fuzzy Logic Systems (T2FUZZ), 
	2011 IEEE Symposium on. IEEE, 2011.

	Arguments:
	----------
	gt2fs -- the general type 2 fuzzy set
	precision -- the precision applied when computing N/D and F
	information -- the amount of information given to the user;
		none - no information
	'''
	reduced_set = None

	if information == 'none':
		reduced_set = _gt2_partialcentroid_noinfo(gt2fs, precision)

	return reduced_set

def _gt2_partialcentroid_noinfo(gt2fs, precision=5):
	# previous partial centroid, C(k-1)
	# initialized so that values of n=1 can be included
	partial_centroid = {(0,0):1}
	# current partial centroid, C(k)
	partial_centroid_copy = {}
	new_N = 0
	new_D = 0
	newDom = 0

	# get each vertical slice
	for primary_domain in gt2fs.primary_domain():
		vertical_slice = gt2fs[primary_domain]

		# get each point in the vertical slice
		for secondary_domain, dom in vertical_slice.elements().items():
			ux = secondary_domain * primary_domain
			
			# process each point in the slice to the corresponding N D F
			for ND, F in partial_centroid.items():

				new_N = round(ND[0] + ux, 5)
				new_D = round(ND[1] + secondary_domain, 5)
				newDom = min(F, dom)

				# pruning
				# for two elements having the dame N and D remove the smallest F
				if (new_N, new_D) in partial_centroid_copy:
					partial_centroid_copy[(new_N, new_D)] = max(partial_centroid_copy[(new_N, new_D)], newDom)
				else:
					partial_centroid_copy[(new_N, new_D)] = newDom

		# move the current to the old
		# and clear the current
		partial_centroid = dict(partial_centroid_copy)
		partial_centroid_copy.clear()

	# create the type reduced set
	type_reduced_set = Type1FuzzySet()

	# go through all NDFs
	for ND, F in partial_centroid.items():
		if ND[1] != 0:
			type_reduced_set.add_element(ND[0]/ND[1], F)

	return type_reduced_set
